import socket
import os


def start_server(host, port, save_dir):
    """
    Start a server.
    :param host: Server IP address
    :param port: Server port
    :param save_dir: Directory to save the received files
    :return:
    """
    # Create the save directory if it does not exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started at {host}:{port}, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection accepted from {addr}")

        # Receive the file name
        file_name = client_socket.recv(1024).decode()
        file_path = os.path.join(save_dir, file_name)

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File {file_name} already exists, not overwritten.")
            client_socket.send(b"File exists")
            client_socket.close()
            continue
        else:
            client_socket.send(b"Ready to receive")

        # Receive the file data
        with open(file_path, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"File {file_name} received successfully.")
        client_socket.close()


if __name__ == "__main__":
    server_host = input("Enter the server host (default: localhost): ") or 'localhost'
    server_port = input("Enter the server port (default: 12345): ")
    server_port = int(server_port) if server_port else 12345
    file_path = input("Enter the path to save the received files: ")
    start_server(host=server_host, port=server_port, save_dir=file_path)
