import socket
import threading

# Configuration
LISTEN_PORT = 8081  # Each peer listens on a unique port (8079, 8080, 8081 for example)
PEER_LIST = [('172.18.13.109', 8080), ('172.18.6.231', 8079)]  # List of known peers

# Function to handle incoming connections (Server Part)
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", LISTEN_PORT))
    server_socket.listen(5)
    print(f"[SERVER] Listening on port {LISTEN_PORT}..")
    while True:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Connection established with {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

# Function to handle communication with connected clients
def handle_client(conn):
    while True:
        try:
            message = conn.recv(1024).decode().strip()
            if not message:
                break
            print(f"[SERVER] Received: {message}")
            conn.send(message.upper().encode())  # Echo back in uppercase
            if message.lower() == "quit":
                break
        except:
            break
    conn.close()

# Function to send messages to multiple peers (Client Part)
def client():
    while True:
        message = input("Type a message: ")
        for peer_ip, peer_port in PEER_LIST:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((peer_ip, peer_port))
                client_socket.send(message.encode())
                response = client_socket.recv(1024).decode()
                print(f"[CLIENT] Received from {peer_ip}:{peer_port}: {response}")
                client_socket.close()
            except:
                print(f"[CLIENT] Could not connect to {peer_ip}:{peer_port}")
        if message.lower() == "quit":
            return

# Start both server and client threads
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=client, daemon=False).start()