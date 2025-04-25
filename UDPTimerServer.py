# UDP Server (simple echo code in Python)
import socket

# Server configuration (hardcoded port)
UDP_IP = "134.88.130.155"  # Use localhost or replace with specific IP if needed
UDP_PORT = 8080  # Hardcoded port

# Create a UDP server socket (AF_INET for IPv4 protocols, SOCK_DGRAM for UDP)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
serverSocket.bind((UDP_IP, UDP_PORT))

print(f"UDP Server is running on {UDP_IP}:{UDP_PORT}")
running = True

while running:
    print(f"UDP Server is waiting for data on port {UDP_PORT}...")
    
    # Receive a message from the client
    message, clientAddress = serverSocket.recvfrom(1024)
    message = message.decode().strip()  # Decode the message to string
    print(f"Received message: '{message}' from {clientAddress}")
    
    # Echo the message back in uppercase
    serverSocket.sendto(message.upper().encode(), clientAddress)
    
    # Shut down the server upon client request
    if message.lower() == 'shutdown':
        running = False
        print("Shutdown command received. Stopping the server...")

# Close the socket
serverSocket.close()
print("UDP Server has shut down.")