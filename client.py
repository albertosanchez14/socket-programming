import sys
from socket import *


class Client:
    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = None

    def initiate_negotiation(self, req_code):
        print('Stage 1. Negotiation using TCP sockets')
        # Open a TCP connection with the server
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))
        print('Connected to the server:', self.serverName, self.serverPort)
        # Send the request code to the server
        print('Initiate Negotiation:', req_code)
        self.clientSocket.send(req_code.encode())
        # Receive the response from the server
        received_message = self.clientSocket.recvfrom(1024)
        # Check if the message is valid
        if received_message[0].decode() == 'Invalid request code':
            print('Invalid request code')
            self.clientSocket.close()
            sys.exit(1)
        # Get the new port number
        r_port = received_message[0].decode()
        print('Contact Port:', r_port)
        # Change to the new r_port and open an UDP connection
        self.clientSocket.close()
        self.serverPort = int(r_port)
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.connect((self.serverName, self.serverPort))

    def send_message(self, msg):
        print('\nStage 2. Transaction using UDP sockets')
        # Send the message to the server
        self.clientSocket.send(msg.encode())
        print('Do something on:', msg)
        # Receive the response from the server
        modifiedMessage, serverAddress = self.clientSocket.recvfrom(1024)
        print('Reply:', modifiedMessage.decode())
        # Close the connection
        self.clientSocket.close()


if __name__ == '__main__':
    # Check if the number of arguments is correct
    if len(sys.argv) != 5:
        print('Usage: python client.py <server_address> <n_port> <req_code> <msg>')
        sys.exit(1)
    # Check if the argument format is correct
    if not sys.argv[2].isdigit():
        print('Invalid port number')
        sys.exit(1)
    if int(sys.argv[2]) < 1024 or int(sys.argv[2]) > 65535:
        print('Invalid port number')
        sys.exit(1)
    if not sys.argv[3].isdigit():
        print('Invalid request code')
        sys.exit(1)
    # Get the server IP, port number and request code
    server_address = sys.argv[1]
    n_port = int(sys.argv[2])
    req_code = sys.argv[3]
    msg = sys.argv[4]
    # Create a client object
    client = Client(server_address, n_port)
    # Initiate negotiation with the server
    client.initiate_negotiation(req_code)
    # Send the message to the server
    client.send_message(msg)
