from commons import *
from time import sleep, time
import socket
import threading
TMP = "!TMP!"
connected_clients = {}
connected_clients_udp = {}

def accept_client(client_socket, addr, conn_type):
    # client_socket.sendall("You have manage to connect to SERVER")
    if conn_type == "TCP": clients = connected_clients
    elif conn_type == "UDP": clients = connected_clients_udp
    while True:
        try:
            msg = client_socket.recv(1024)
            print(f"SERVER: Client{addr[1]} has sent message: \"{msg}\"")
            # client_socket.sendall(bytes(f"Your msg: {msg}", encoding='utf-8'))
            for client in clients.items():
                clinet_id = client[0]
                client_conn = client[1]
                if clinet_id != addr[1]: 
                    client_conn.sendall(bytes(f"{addr[1]}, NICKNAME: {msg}", encoding='utf-8'))
        except Exception as e:
            print(f"SERVER WARNING: Client({addr[1]}) closed connection!")
            #remove client from "database"
            if conn_type == "TCP":
                del connected_clients[addr[1]]
            elif conn_type == "UDP":
                del connected_clients_udp[addr[1]]
            client_socket.close()
            return
    
def accepting_thread(soc, conn_type):
    try:
        print(f"SERVER: Server waits for connection...")
        con, addr = soc.accept()
        print(f"SERVER: New connection on {conn_type} socket from addr={addr}")
        if conn_type == "TCP":
            connected_clients[addr[1]] = con
        elif conn_type == "UDP":
            connected_clients_udp[addr[1]] = con
        t = threading.Thread(target=accept_client, args=(con, addr, conn_type))
        t.daemon = True
        t.start()
    except Exception as e:
        print(f"SERVER ERROR: {e}")


print(f"SERVER: Server is starting it's job...")
#Creates TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((SERVER_IP, PORT))
soc.listen(5)

#Creats UDP socket
soc_udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_udp.bind((SERVER_IP, PORT))
soc_udp.listen(5)

#Creating threads handling connections depending on socket type
t_tcp = threading.Thread(target=accepting_thread, args=(soc, "TCP",))
t_udp = threading.Thread(target=accepting_thread, args=(soc, "UDP",))

threads = [t_tcp, t_udp]

for t in threads:
    t.daemon = True
    t.start()

#Main thread infinite loop
while True:
    try:
        sleep(0.1)
    except Exception as e:
        print(f"SERVER INTERRUPTION: {e}")
        break

#Finishing up
soc.close()
soc_udp.close()

#All Threads are set to be daemon so they will die as soon as main Thread is killed.