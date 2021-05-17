import kazoo
from kazoo.client import KazooClient
from kazoo.client import KazooState

from time import sleep
SLEEP_TIME = 0.5

import random
import string

import logging
logging.basicConfig()
global_set = set()

import keyboard as kb

def get_random_string_bytes(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return bytes(result_str, encoding="utf-8")

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print("Session has been lost.")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print("Session has been disconnedted.")
    else:
        # Handle being connected/reconnected to Zookeeper
        print("Connected.")

first = True
zk = KazooClient(hosts='127.0.0.1:11500')
zk.add_listener(my_listener)
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