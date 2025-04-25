import socket
import threading

# Configuration
LISTEN_PORT = 9091  # Each peer listens on a unique port (9090, 9091, 9092 for example)
PEER_LIST = [('172.18.6.231', 9090), ('172.18.13.109', 9092)]  # List of known peers

# Function to handle incoming messages (Server Part)
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", LISTEN_PORT))
    print(f"[SERVER] Listening on port {LISTEN_PORT}...")

    while True:
        message, addr = server_socket.recvfrom(1024)
        print(f"[SERVER] Received from {addr}: {message.decode()}")
        server_socket.sendto(message.upper(), addr)  # Echo back in uppercase

# Function to send messages to multiple peers (Client Part)
def client():
    while True:
        message = input("Type a message: ")
        for peer_ip, peer_port in PEER_LIST:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client_socket.sendto(message.encode(), (peer_ip, peer_port))
                response, _ = client_socket.recvfrom(1024)
                print(f"[CLIENT] Received from {peer_ip}:{peer_port}: {response.decode()}")
            except:
                print(f"[CLIENT] Could not send to {peer_ip}:{peer_port}")
        
        if message.lower() == "quit":
            return

# Start both server and client threads
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=client, daemon=False).start()