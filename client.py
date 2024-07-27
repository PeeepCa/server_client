import socket
import os


def send_file(server_host, server_port, file_path):
    """
    Client function
    :param server_host: Server IP address
    :param server_port: Server port
    :param file_path: Path to file to be sent
    :return:
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode())

    response = client_socket.recv(1024).decode()
    if response == "File exists":
        print(f"File {file_name} already exists on the server.")
        client_socket.close()
        return

    # Send the file data
    with open(file_path, 'rb') as f:
        while (data := f.read(1024)):
            client_socket.send(data)
            print(f"Sent {len(data)} bytes")

    print(f"File {file_name} sent successfully.")
    client_socket.close()


if __name__ == "__main__":
    server_host = input("Enter the server host (default: localhost): ") or 'localhost'
    server_port = input("Enter the server port (default: 12345): ")
    server_port = int(server_port) if server_port else 12345
    file_path = input("Enter the path to the file you want to send: ")

    send_file(server_host, server_port, file_path)