import socket
import threading

# Configuration
LISTEN_PORT = 9099  # Unique port for this peer
PEER = ('134.85.140.155', 9091)  # Single known peer (fixed IP format)

# Function to handle incoming messages (Server Part)
def peer_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", LISTEN_PORT))
    print(f"[PEER] Listening on port {LISTEN_PORT}...")
    
    while True:
        try:
            message, addr = server_socket.recvfrom(1024)
            print(f"[PEER] Received from {addr}: {message.decode()}")
            # Echo back the message in uppercase
            server_socket.sendto(message.upper(), addr)
        except Exception as e:
            print(f"[PEER] Error receiving message: {e}")
            break

# Function to send messages to a single peer (Client Part)
def peer_client():
    while True:
        message = input("Type a message: ")
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(message.encode(), PEER)
            
            # Wait for response (optional)
            response, _ = client_socket.recvfrom(1024)
            print(f"[PEER] Received response: {response.decode()}")
            
            if message.lower() == "quit":
                break
                
        except Exception as e:
            print(f"[PEER] Could not send to {PEER[0]}:{PEER[1]} - {e}")

# Start both server and client threads
server_thread = threading.Thread(target=peer_server, daemon=True)
server_thread.start()
peer_client()  # Run client in main thread