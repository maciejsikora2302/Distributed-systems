import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.5", 55000))
msg, addr = s.recvfrom(1024)
print(f"msg = {msg.decode('utf-8')}, addr = {addr} ")
s.sendto(bytes("response0", encoding='utf-8'), addr)
s.close()