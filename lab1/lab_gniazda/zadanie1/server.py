from commons import *
from time import sleep, time
import socket
import threading
TMP = "!TMP!"
UDP = "UDP"
TCP = "TCP"

def handle_client(client_socket, addr, nickname, connected_clients):
    # client_socket.sendall("You have manage to connect to SERVER")
    # print(connected_clients)
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            print(f"SERVER: Client id[{addr[1]}], nickname:[{nickname}] has sent a message [{msg}]")
            # if conn_type == "TCP": client_socket.sendall(bytes(addr[1]))
            # client_socket.sendall(bytes(f"Your msg: {msg}", encoding='utf-8'))

            for client in connected_clients.items():
                client_id, connection = client[0][1], client[1]
                if client_id != addr[1]: 
                    print(f"SERVER: Sending msg[{msg}] from {addr} to {client_id}")
                    connection.sendall(bytes(f"{addr[1]}, {nickname}: {msg}", encoding='utf-8'))
        except Exception as e:
            print(f"SERVER WARNING: Client({addr[1]}) closed connection!")
            #remove client from "database"
            del connected_clients[addr]
            client_socket.close()
            return

# def handle_clients_udp(sock, nickname, connected_clients):
#     while True:
#         msg, conn = sock.recvfrom(1024)
#         msg = msg.decode('utf-8')
#         print(f"SERVER: msg on upd {msg}")
#         for client in connected_clients:
#             if client != conn:
#                 print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {client}")
#                 print(f"SERVER: Sending msg[{msg}] from {sock} to {conn}")
#                 sock.sendto(bytes(f"{nickname}: {msg}", encoding='utf-8'), client)
def tcp_server():
    connected_clients = {}
    #Creates TCP socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((SERVER_IP, PORT))
    soc.listen(5)

    while True:
        try:
            print(f"SERVER: Server waits for connection on TCP...")
            con, addr = soc.accept()
            print(f"SERVER: New connection on TCP socket from addr={addr}")

            #send client id to the client
            con.sendall(bytes(str(addr[1]),encoding='utf-8'))
            #receive his nickname
            nickname = con.recv(1024).decode('utf-8')

            connected_clients[addr] = con
            print(f"SERVER NEW CONNECTION: current connections: {connected_clients.items()}")
            
            t = threading.Thread(target=handle_client, args=(con, addr, nickname, connected_clients))
            t.daemon = True
            t.start()
        except Exception as e:
            print(f"SERVER ERROR: {e}")
            break

def udp_server():
    connected_clients = set()
    soc_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc_udp.bind((SERVER_IP_UDP, PORT_UDP))
    while True:
        try:
            print(f"SERVER: Server waits for msg on UDP...")
            msg, addr_udp = soc_udp.recvfrom(1024)
            msg = msg.decode('utf-8', "backslashreplace")
            if msg == "&&FIRST&&":
                print("New connection")
                nickname, addr_udp = soc_udp.recvfrom(1024)
                connected_clients.add((addr_udp, nickname.decode('utf-8')))
            else:
                final_msg = ""
                final_msg += msg
                while msg[-2:] != "-F":
                    print(f"receiving more..., current msg {msg}")
                    msg, addr_udp = soc_udp.recvfrom(1024)
                    msg = msg.decode('utf-8', "backslashreplace")
                    final_msg += msg
                print(f"UDP SERVER: msg on upd {final_msg}")
                for client in connected_clients:
                    if client[0] != addr_udp:
                        print(f"SERVER: Sending msg[{final_msg}] from udpsock to {client}")
                        send_in_fragments(final_msg, soc_udp, client[0])
                        # soc_udp.sendto(bytes(f"{client[1]}: {msg}", encoding='utf-8'), client[0])            
            # print(f"SERVER: New connection on UDP socket from addr={addr_udp}")
            # connected_clients.add(addr_udp)
            # print(f"SERVER NEW CONNECTION: current connections UDP: {connected_clients}")

            # #receive his nickname
            # nickname = nickname.decode('utf-8')
            
            # t = threading.Thread(target=handle_clients_udp, args=(soc_udp, nickname, connected_clients))
            # t.daemon = True
            # t.start()
        except Exception as e:
            print(f"SERVER ERROR UDP: {e}")
            break

print(f"SERVER: Server is starting its job...")

#Creats UDP socket


#Creating threads handling connections depending on socket type
tcp_serv_t = threading.Thread(target=tcp_server)
udp_serv_t = threading.Thread(target=udp_server)

tcp_serv_t.daemon = True
udp_serv_t.daemon = True

tcp_serv_t.start()
udp_serv_t.start()

while True:
    try:
        sleep(0.1)
    except Exception as e:
        print(f"SERVER CLOSING {e}")
        break


#Finishing up
# soc.close()
# soc_udp.close()

#All Threads are set to be daemon so they will die as soon as main Thread is killed.