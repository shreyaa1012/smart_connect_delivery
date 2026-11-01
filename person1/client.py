import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
COMMAND = sys.argv[3]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.settimeout(5)

try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Server is unavailable.")
    client_socket.close()
    sys.exit()
except socket.timeout:
    print("Connection timed out.")
    client_socket.close()
    sys.exit()

print("Connected to server on port", PORT)

if COMMAND == "HEALTH":
    request = "HEALTH"

else:
    request = "GET " + COMMAND

try:
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode()

    print("Server response:", response)

except socket.timeout:
    print("Server response timed out.")

client_socket.close()

print("Client closed.")