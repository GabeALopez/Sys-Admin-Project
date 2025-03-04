import socket

def start_client():
    # Create a socket object to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'  # Localhost
    port = 12345         # Port number

    # Connect to the server
    client_socket.connect((host, port))

    while True:
        # Input message from the user
        message = input("Enter message to send to server (or 'exit' to quit): ")

        # If the message is 'exit', break the loop and disconnect
        if message.lower() == 'exit':
            print("Closing connection.")
            break

        # Send the message to the server
        client_socket.send(message.encode())

        # Receive the server's response
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode()}")

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    start_client()
