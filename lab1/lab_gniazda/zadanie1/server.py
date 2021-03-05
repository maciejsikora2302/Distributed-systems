from commons import *
from time import sleep, time
import socket
import threading
TMP = "!TMP!"
connected_clients = {}

def accept_client(client_socket, addr):
    print(f"SERVER: New connection, addr={addr}")
    # client_socket.sendall("You have manage to connect to SERVER")
    while True:
        try:
            msg = client_socket.recv(1024)
            print(f"SERVER: Client{TMP} has sent message: \"{msg}\"")
            client_socket.sendall(bytes(f"Your msg: {msg}", encoding='utf-8'))
        except Exception as e:
            print(f"SERVER WARNING: Client({addr[1]}) closed connection!")
            del connected_clients[addr]
            client_socket.close()
            return
    

#Creates TCP socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((SERVER_IP, PORT))
soc.listen(5)
#Setting timeout
# soc.settimeout(5)

print(f"SERVER: Server is starting it's job...")
while True:
    try:
        print(f"SERVER: Server waits for connection...")
        con, addr = soc.accept()
        connected_clients[addr] = con
        t = threading.Thread(target=accept_client, args=(con, addr,))
        t.start()
    except Exception as e:
        print(f"SERVER ERROR: {e}")
