import socket
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))
print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")
while True:
 data, addr = server_socket.recvfrom(1024)
 print(f"Received message: {data.decode()} from {addr}")
 server_socket.sendto(data, addr)