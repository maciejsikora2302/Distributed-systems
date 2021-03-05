from commons import *
from time import sleep, time
import socket
import threading
TMP = "!TMP!"
connected_clients = {}
connected_clients_udp = {}

def accept_client(client_socket, addr, conn_type, nickname, connected_clients):
    # client_socket.sendall("You have manage to connect to SERVER")
    print(connected_clients)
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            print(f"SERVER: Client id[{addr[1]}], nickname:[{nickname}] has sent a message [{msg}]")
            # if conn_type == "TCP": client_socket.sendall(bytes(addr[1]))
            # client_socket.sendall(bytes(f"Your msg: {msg}", encoding='utf-8'))
            if conn_type == "TCP": 
                for client in connected_clients.items():
                    clinet_id = client[0][1]
                    client_conn = client[1]
                    if clinet_id != addr[1]: 
                        print(f"SERVER: Sending msg[{msg}] from {addr} to {clinet_id}")
                        client_conn.sendall(bytes(f"{addr[1]}, {nickname}: {msg}", encoding='utf-8'))
            elif conn_type == "UDP": 
                for client in connected_clients_udp.items():
                    clinet_id = client[0]
                    client_conn = client[1]
                    if clinet_id != addr[1]: 
                        client_conn.sendall(bytes(f"{addr[1]}, {nickname}: {msg}", encoding='utf-8'))
        except Exception as e:
            print(f"SERVER WARNING: Client({addr[1]}) closed connection!")
            #remove client from "database"
            del connected_clients[addr]
            client_socket.close()
            return
    
def accepting_thread(soc, conn_type, connected_clients):
    while True:
        try:
            print(f"SERVER: Server waits for connection on {conn_type}...")
            con, addr = soc.accept()
            print(f"SERVER: New connection on {conn_type} socket from addr={addr}")
            if conn_type == "TCP":
                #send client id to the client
                con.sendall(bytes(str(addr[1]),encoding='utf-8'))
                #receive his nickname
                nickname = con.recv(1024).decode('utf-8')
            connected_clients[addr] = con
            print(f"SERVER NEW CONNECTION: current connections on {conn_type}: {connected_clients.items()}")
            
            t = threading.Thread(target=accept_client, args=(con, addr, conn_type, nickname, connected_clients))
            t.daemon = True
            t.start()
        except Exception as e:
            print(f"SERVER ERROR: {e}")
            return


print(f"SERVER: Server is starting its job...")
#Creates TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((SERVER_IP, PORT))
soc.listen(5)

#Creats UDP socket
soc_udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_udp.bind((SERVER_IP, PORT_UDP))
soc_udp.listen(5)

#Creating threads handling connections depending on socket type
t_tcp = threading.Thread(target=accepting_thread, args=(soc, "TCP", connected_clients))
t_udp = threading.Thread(target=accepting_thread, args=(soc, "UDP", connected_clients_udp))

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