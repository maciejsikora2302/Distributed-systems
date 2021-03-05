from commons import *
from time import time, sleep
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))

while True:
    try:
        s.sendall(bytes('Hello, world', encoding='utf-8'))
        msg = s.recv(1024)
        print(f"CLIENT: Callback from server: {msg}")
        sleep(1)
    except Exception as e:
        print(f"CLIENT ERROR: {e}")
        break
s.close()