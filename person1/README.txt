PERSON 1 – TCP CONTENT DELIVERY

Project: Smart Content Delivery System

Files:
- server.py
- client.py

SERVER

Start Server 1:
python server.py Server1 5001

Start Server 2:
python server.py Server2 5002


CLIENT

Request content from Server 1:
python client.py 5001 file1

Request content from Server 2:
python client.py 5002 file1


SUPPORTED REQUESTS

HEALTH
GET file1
GET file2
GET file3


FEATURES IMPLEMENTED

- TCP client-server communication
- Content request and response
- Multiple content servers
- Multiple client connections using threading
- Server health checking
- Invalid content handling
- Server unavailable handling
- Connection timeout handling
- Server failure and recovery
- Content delivery from multiple servers


TESTING COMPLETED

- file1, file2 and file3 content delivery
- HEALTH request
- Invalid content request
- Multiple clients
- Multiple servers
- Server failure
- Server recovery
- Connection error handling


NOTE

The current version uses localhost (127.0.0.1) for local application testing.

For Mininet/SDN integration, the client and server can later be adapted to use Mininet host IP addresses.