import socket
import sys
import threading

HOST = "0.0.0.0"

SERVER_NAME = sys.argv[1]
PORT = int(sys.argv[2])


def handle_client(client_socket, client_address):
    print("Client connected:", client_address)

    request = client_socket.recv(1024).decode()

    print("Client requested:", request)

    content_repository = {
        "file1": "This is the content of file1 from " + SERVER_NAME,
        "file2": "This is the content of file2 from " + SERVER_NAME,
        "file3": "This is the content of file3 from " + SERVER_NAME
    }

    if request == "HEALTH":
        response = SERVER_NAME + " is healthy."

    elif request.startswith("GET "):
        content_name = request[4:]

        if content_name in content_repository:
            response = content_repository[content_name]
        else:
            response = "Content not found."

    else:
        response = "Invalid request."

    client_socket.send(response.encode())

    client_socket.close()

    print("Client served:", client_address)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(SERVER_NAME, "is running...")
print("Listening on port:", PORT)
print("Waiting for clients...")


while True:
    client_socket, client_address = server_socket.accept()

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )

    client_thread.start()