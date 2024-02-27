import sys
import random
from socket import *


class Server:
    def __init__(self, port, req_code):
        self.serverPort = port
        self.req_code = req_code
        # Create TCP welcoming socket
        self.serverSocket_TCP = socket(AF_INET, SOCK_STREAM)
        self.serverSocket_TCP.bind(('', self.serverPort))
    
    def negotiation_stage(self) -> None:
        print('Stage 1. Negotiation using TCP sockets')
        # Listen for incoming connections
        self.serverSocket_TCP.listen(1)
        # Accept the incoming connection
        connectionSocket, addr = self.serverSocket_TCP.accept()
        req_code_cl = connectionSocket.recv(1024).decode()
        print('Initiate Negotiation:', req_code_cl)
        # Check if the message is valid
        if req_code_cl != self.req_code:
            connectionSocket.send('Invalid request code'.encode())
            connectionSocket.close()
            self.negotiation_stage()
        r_code = random.randint(1024, 2000)
        # Check if the port is not in use
        while Server.__is_port_in_use(r_code):
            r_code = random.randint(1024, 2000) 
        print('Contact Port:', r_code)
        # Send the response to the client
        connectionSocket.send(str(r_code).encode())
        # Close the connection to the client
        connectionSocket.close()
        # Continue to the transaction stage
        self.transaction_stage(r_code)
    
    def transaction_stage(self, r_code: int) -> None:
        print('\nStage 2. Transaction using UDP sockets')
        # Open a UDP connection with the client
        self.serverSocket_UDP = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket_UDP.bind(('', r_code))
        msg = None
        clientAddress = None
        while msg is None:
            # Receive the message from the client
            message_enc, clientAddress = self.serverSocket_UDP.recvfrom(1024)
            msg = message_enc.decode()
            print('Do something on:', msg)
        # Reverse the string and send
        modifiedMessage = msg[::-1]
        print('Reply:', modifiedMessage)
        print('\n')
        self.serverSocket_UDP.sendto(modifiedMessage.encode(), clientAddress)
        # Close the connection
        self.serverSocket_UDP.close()
        # Continue listening for incoming connections
        self.negotiation_stage()

    def __is_port_in_use(port: int) -> bool:
        with socket(AF_INET, SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0


if __name__ == '__main__':
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print('Usage: python server.py <n_port> <req_code>')
        sys.exit(1)
    # Check if the argument format is valid
    if not sys.argv[1].isdigit():
        print('Invalid port number')
        sys.exit(1)
    if not sys.argv[2].isdigit():
        print('Invalid request code')
        sys.exit(1)
    if int(sys.argv[1]) < 1024 or int(sys.argv[1]) > 65535:
        print('Invalid port number')
        sys.exit(1)
    # Get the port number and request code
    n_port = int(sys.argv[1])
    req_code = sys.argv[2]
    # Create a server object and start the server
    server = Server(n_port, req_code).negotiation_stage()
