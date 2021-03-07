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

def receive_msg_udp(soc):
    # print("awaiting for msg from server")
    while True:
        try:
            final_msg = ""
            msg, addr = soc.recvfrom(1024)
            msg = msg.decode('utf-8', "backslashreplace")
            while msg[-2:] != "-F":
                final_msg += msg
                msg, addr = soc.recvfrom(1024)
                msg = msg.decode('utf-8', "backslashreplace")

            final_msg += msg
            # print(f"CLIENT: Incoming message-> {msg.decode('utf-8')}")
            final_msg = final_msg.replace('\\n', '\n')
            print(f"{final_msg}")
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return

def send_msg(soc, soc_udp):
    while True:
        try:
            # print(f"{my_id}, {nickname}: ", end='')
            msg = input()
            # print(f"CLIENT: Sending message-> {msg}")
            if msg[:2] == "-U":
                to_add = input()
                while to_add != "-F":
                    print("adding")
                    msg += to_add
                    to_add = input()
                msg += to_add
                print("finished adding")
                send_in_fragments(msg, s_udp, (SERVER_IP_UDP, PORT_UDP))
                # s_udp.sendto(bytes(msg, encoding='utf-8'), (SERVER_IP_UDP, PORT_UDP))
            elif msg[:2] == "-M":
                pass
            else:
                soc.sendall(bytes(msg, encoding='utf-8'))
            
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return


#Generating random nickname
nickname = NICKNAMES[randint(0, len(NICKNAMES))] #input()

#Tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT: Connecting on TCP socket")
s.connect((SERVER_IP, PORT))
print("CLIENT: Connected, awaiting for my id...")
my_id = s.recv(1024).decode('utf-8')
print(f"CLIENT: my_id: {my_id}")
print(f"CLIENT: Sending my nick({nickname})...")
s.sendall(bytes(f'{nickname}', encoding='utf-8'))
print(f"CLINET: Nicnkname sent!")


#Udp socket
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("CLIENT: Connecting on UDP socket")
s_udp.sendto(bytes(f'&&FIRST&&', encoding='utf-8'), (SERVER_IP_UDP, PORT_UDP))
s_udp.sendto(bytes(f'{nickname}', encoding='utf-8'), (SERVER_IP_UDP, PORT_UDP))
print("CLIENT: Connected and Nicnkname sent!")




#Handling receving and sending
sending_thread = threading.Thread(target=send_msg, args=(s, None))
receive_thread = threading.Thread(target=receive_msg, args=(s,))
receive_thread_udp = threading.Thread(target=receive_msg_udp, args=(s_udp,))

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