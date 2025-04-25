from socket import *
import time

# Server configuration (hardcoded to match server)
SERVER_IP = "134.88.130.155"  # Change to match your server's IP if necessary
SERVER_PORT = 8080            # Hardcoded port to match the server
TIMEOUT = 10                  # 10 second timeout for the socket

# Create a UDP client socket (AF_INET for IPv4 protocols, SOCK_DGRAM for UDP)
clientSocket = socket(AF_INET, SOCK_DGRAM)

print(f"UDP Client is running. Sending messages to {SERVER_IP}:{SERVER_PORT}")

# Client takes message from user input, sends it to the server, and receives its echo
while True:
    message = input("Type a message (or 'quit' to exit): ")
    clientSocket.settimeout(TIMEOUT)

    try:
        # Record send time
        send_time = time.time()
        
        # Send the UDP packet to the server
        clientSocket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        
        # Receive the server response
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        
        # Record receive time
        receive_time = time.time()

        # Print the echoed message and round-trip time (RTT)
        rtt = receive_time - send_time
        print(f"Received echo: {modifiedMessage.decode()} in RTT: {rtt:.6f} seconds")

    except timeout:
        # Server did not respond, assume the packet is lost
        print("Timeout! Message may be lost.")

    # Exit the loop if the message is 'quit' or 'shutdown'
    if message.lower() == 'quit' or message.lower() == 'shutdown':
        print("Client quitting!")
        break

# Close the client socket
clientSocket.close()
print("UDP Client has shut down.")