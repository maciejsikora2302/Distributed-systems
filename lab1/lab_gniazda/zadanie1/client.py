from commons import *
from time import time, sleep
import threading
import socket
import sys
from random import randint

def receive_msg(soc):
    while True:
        try:
            msg = soc.recv(1024)
            print(f"{msg.decode('utf-8')}") #Display received message
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return

def receive_msg_udp(soc):
    while True:
        try:
            final_msg = ""
            msg, addr = soc.recvfrom(1024)
            msg = msg.decode('utf-8')
            if msg[:2] == "-U" or msg[:2] == "-M":
                msg = msg[2:]
            while msg[-3:-1] != "-F": #At the end there is always \n
                final_msg += msg
                msg, addr = soc.recvfrom(1024)
                msg = msg.decode('utf-8')

            final_msg += msg[:-3] #Delete -F flag
            print(f"{final_msg}") #Display message
        except Exception as e:
            print(f"CLIENT ERROR: {e}")
            return

def send_msg(soc, soc_udp, soc_multi):
    while True:
        try:
            msg = input()
            #Parsing message depending on provided flag (optional argument)
            if msg[:2] == "-U":
                to_add = input()
                while to_add != "-F":
                    msg += to_add + '\n'
                    to_add = input()
                msg += to_add + '\n'
                send_in_fragments(msg, soc_udp, (SERVER_IP_UDP, PORT_UDP))
            elif msg[:2] == "-M":
                to_add = input()
                while to_add != "-F":
                    msg += to_add + '\n'
                    to_add = input()
                msg += to_add + '\n'
                send_in_fragments_multi(msg, soc_multi, (MCAST_GRP, MCAST_PORT))
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

#Multicast socket
import struct
s_multi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s_multi.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_multi.bind(('', MCAST_PORT)) #Listen to everything that is happening on this socket
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s_multi.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


#Handling receving and sending
sending_thread = threading.Thread(target=send_msg, args=(s, s_udp, s_multi))
receive_thread = threading.Thread(target=receive_msg, args=(s,))
receive_thread_udp = threading.Thread(target=receive_msg_udp, args=(s_udp,))
receive_thread_multi = threading.Thread(target=receive_msg_udp, args=(s_multi,))

#Starting Threads and setting them to be daemons so when main thread will die they will be killed as well
threads = [sending_thread, receive_thread, receive_thread_udp, receive_thread_multi]
for t in threads:
    t.daemon = True
    t.start()

while True:
    try:
        sleep(0.1)
    except Exception as e:
        print(f"CLIENT ERROR: {e}")
s.close()