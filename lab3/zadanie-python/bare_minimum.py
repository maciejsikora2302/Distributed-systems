import kazoo
from kazoo.client import KazooClient
from kazoo.client import KazooState

import keyboard as kb

global_set = set()

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

if zk.exists("/z"):
    print("Cleaning up. z_path")
    zk.delete("/z", recursive=True)

def print_structure():
    global global_set
    t = [i for i in global_set]
    t.sort()
    for item in t:
        print(item)

kb.add_hotkey('ctrl+[', print_structure)

def watcher(event):
    global global_set
    if event.type == kazoo.protocol.states.EventType.CREATED:
        zk.exists(event.path, watch=watcher)
        zk.get_children(event.path, watch=watcher)
        if event.path not in global_set:
            global_set.add(event.path)
            print(f"Number of children -> {len(global_set)}")
    elif event.type == kazoo.protocol.states.EventType.CHILD:
        if zk.exists(event.path, watch=watcher):
            children = zk.get_children(event.path, watch=watcher)
            for child in children:
                child_path = f"{event.path}/{child}"
                zk.exists(child_path, watch=watcher)
                zk.get_children(child_path, watch=watcher)
                if child_path not in global_set:
                    global_set.add(child_path)
                    print(f"Number of children -> {len(global_set)}")
    elif event.type == kazoo.protocol.states.EventType.DELETED:
        zk.exists(event.path, watch=watcher)
        if event.path in global_set: 
            global_set.remove(event.path)
            print(f"Number of children -> {len(global_set)}")
      
zk.exists("/z", watch=watcher)

try:
    while True: 
        pass
except KeyboardInterrupt:
    zk.stop()
    print("Finished.")
    exit()

zk.stop()
print("Finished.")