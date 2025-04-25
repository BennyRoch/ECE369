import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))  # Fixed parentheses
server_socket.listen(1)
print(f"TCP server listening on {TCP_IP}:{TCP_PORT}")  # Changed printf to print

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")  # Changed printf to print
        
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received message: {data.decode()}")  # Changed printf to print
                conn.sendall(data)  # Echo back the data
        finally:
            conn.close()
            print(f"Closed connection with {addr}")  # Added connection close message
            
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()
    print("Server socket closed")