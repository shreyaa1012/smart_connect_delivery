import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
COMMAND = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5)

try:
    client_socket.connect((HOST, PORT))

    print("Connected to server on port", PORT)

    if COMMAND == "HEALTH":
        request = "HEALTH"
    else:
        request = "GET " + COMMAND

    client_socket.sendall(request.encode())

    response = client_socket.recv(1024)

    if not response:
        print("Server disconnected without sending a response.")
    else:
        print("Server response:", response.decode())

except ConnectionRefusedError:
    print("Server is unavailable.")

except socket.timeout:
    print("Connection or response timed out.")

except ConnectionResetError:
    print("Server disconnected unexpectedly.")

except OSError as error:
    print("Network error:", error)

finally:
    client_socket.close()
    print("Client closed.")