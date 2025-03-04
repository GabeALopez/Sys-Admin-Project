import socket
import json

def start_client():
    # Create a socket object to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'  # Localhost
    port = 12345         # Port number

    # Connect to the server
    client_socket.connect((host, port))

    while True:
        # Prepare data to send as JSON
        message = input("Enter message to send to server (or 'exit' to quit): ")

        # If the message is 'exit', break the loop and disconnect
        if message.lower() == 'exit':
            print("Closing connection.")
            break

        # Create a dictionary to send as JSON
        data_to_send = {"user_message": message, "status": "sending"}
        json_data = json.dumps(data_to_send)

        # Send the message to the server as JSON
        client_socket.send(json_data.encode())

        # Receive the server's response
        response = client_socket.recv(1024)
        
        # Deserialize the JSON response from the server
        try:
            received_response = json.loads(response.decode())
            print(f"Received from server: {received_response}")
        except json.JSONDecodeError:
            print("Error decoding JSON response from server.")
            continue

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    start_client()
