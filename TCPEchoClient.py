import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 5005
MESSAGE = "Hello, TCP Server!"

try:
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((TCP_IP, TCP_PORT))
    print(f"Connected to server at {TCP_IP}:{TCP_PORT}")
    
    # Send message to server
    client_socket.sendall(MESSAGE.encode())
    print(f"Sent message: {MESSAGE}")
    
    # Receive echo response
    data = client_socket.recv(1024)
    print(f"Received echo: {data.decode()}")
    
except ConnectionRefusedError:
    print(f"Could not connect to server at {TCP_IP}:{TCP_PORT}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Ensure socket is closed
    client_socket.close()
    print("Connection closed")