
import socket
import sys
import threading

HOST = "0.0.0.0"

SERVER_NAME = sys.argv[1]
PORT = int(sys.argv[2])


def handle_client(client_socket, client_address):
    print("Client connected:", client_address)

    try:
        client_socket.settimeout(5)

        request = client_socket.recv(1024).decode().strip()

        if not request:
            print("Empty request from:", client_address)
            return

        print("Client requested:", request)

        content_repository = {
            "file1": "This is the content of file1 from " + SERVER_NAME,
            "file2": "This is the content of file2 from " + SERVER_NAME,
            "file3": "This is the content of file3 from " + SERVER_NAME
        }

        if request == "HEALTH":
            response = SERVER_NAME + " is healthy."

        elif request.startswith("GET "):
            content_name = request[4:].strip()

            if content_name in content_repository:
                response = content_repository[content_name]
            else:
                response = "Content not found."

        else:
            response = "Invalid request."

        client_socket.sendall(response.encode())

        print("Client served:", client_address)

    except socket.timeout:
        print("Client request timed out:", client_address)

    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected unexpectedly:", client_address)

    except Exception as error:
        print("Error handling client:", error)

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(SERVER_NAME, "is running...")
print("Listening on port:", PORT)
print("Waiting for clients...")

try:
    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        client_thread.start()

except KeyboardInterrupt:
    print("\nShutting down", SERVER_NAME)

finally:
    server_socket.close()
    print("Server socket closed.")
