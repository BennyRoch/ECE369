import socket
import threading

# Configuration
LISTEN_PORT = 8079  # Port for incoming connections
PEER_IP = '127.0.0.1'  # Change this to the actual peer IP you want to connect to
PEER_PORT = 8080  # Port of another peer

# Function to handle incoming connections (Server Part)
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", LISTEN_PORT))
    server_socket.listen(5)
    print(f"[SERVER] Listening on port {LISTEN_PORT}...")

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

# Function to send messages to another peer (Client Part)
def client():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((PEER_IP, PEER_PORT))
            print(f"[CLIENT] Connected to peer at {PEER_IP}:{PEER_PORT}")

            while True:
                message = input("Type a message: ")
                client_socket.send(message.encode())
                response = client_socket.recv(1024).decode()
                print(f"[CLIENT] Received: {response}")
                if message.lower() == "quit":
                    client_socket.close()
                    return
        except:
            print("[CLIENT] Could not connect. Retrying...")

# Start both server and client threads
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=client, daemon=False).start()