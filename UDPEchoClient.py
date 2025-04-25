import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, UDP Server!"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
data, server = client_socket.recvfrom(1024)
print(f"Received echo: {data.decode()}")