import socket
import threading

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] Client {client_address[0]}:{client_address[1]} connected.")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[ECHO] Received from {client_address[1]}: {data.decode()}")
            client_socket.sendall(data)
    except ConnectionResetError:
        print(f"[DISCONNECT] Client {client_address[0]}:{client_address[1]} disconnected abruptly.")
    finally:
        client_socket.close()
        print(f"[CLOSED] Connection with {client_address[0]}:{client_address[1]} closed.")

def start_server(host="0.0.0.0", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[SERVER STARTED] Listening on port {port}...")

    while True:
        client_socket, client_address = server.accept()
        print(f"[CONNECTION INFO] Server connected on socket port: {client_socket.getsockname()[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()