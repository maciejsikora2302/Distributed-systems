from commons import *
from time import time, sleep
import threading
import socket
import sys
from random import randint

def receive_msg(soc):
    # print("awaiting for msg from server")
    while True:
        try:
            msg = soc.recv(1024)
            # print(f"CLIENT: Incoming message-> {msg.decode('utf-8')}")
            print(f"{msg.decode('utf-8')}")
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return

def send_msg():
    while True:
        try:
            # print(f"{my_id}, {nickname}: ", end='')
            msg = input()
            # print(f"CLIENT: Sending message-> {msg}")
            if msg[:2] == "-U":
                s_udp.sendall(bytes(msg, encoding='utf-8'))
            elif msg[:2] == "-M":
                pass
            else:
                s.sendall(bytes(msg, encoding='utf-8'))
            
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return

#Tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))
print("CLIENT: Connected, awaiting for my id...")
my_id = s.recv(1024).decode('utf-8')
print(f"CLIENT: my_id: {my_id}")

#Udp socket
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_udp.connect((SERVER_IP, PORT_UDP))

#Generating random nickname and sending hello msg to server
nickname = NICKNAMES[randint(0, len(NICKNAMES))] #input()
print(f"CLIENT: Sending my nick({nickname})...")
s.sendall(bytes(f'{nickname}', encoding='utf-8'))
print(f"CLINET: Nicnkname sent!")

#Handling receving and sending
sending_thread = threading.Thread(target=send_msg)
receive_thread = threading.Thread(target=receive_msg, args=(s,))
receive_thread_udp = threading.Thread(target=receive_msg, args=(s_udp,))

#Starting Threads and setting them to be daemons so when main thread will die they will be killed as well
threads = [sending_thread, receive_thread, receive_thread_udp]
for t in threads:
    t.daemon = True
    t.start()

while True:
    try:
        sleep(0.1)
    except Exception as e:
        print(f"CLIENT ERROR: {e}")
s.close()