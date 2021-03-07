import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(bytes("super cool msg", encoding='utf-8'), ("127.0.0.5", 55000))
print(s.recvfrom(1024))
s.close()