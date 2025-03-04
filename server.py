import socket

def start_server():
    # Set up the server to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = '127.0.0.1'  # Localhost
    port = 12345         # Port number

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    # Accept a connection from the client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    # Communication loop
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            print("Client has disconnected.")
            break
        print(f"Received from client: {data.decode()}")

        # Send a response back to the client
        response = "Message received"
        client_socket.send(response.encode())

    # Close the connection
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
