# Socket Programming
This assignment consists in create a client-server architecture where the client stablish a TCP conection with the client to get a port number to subsecuently send through that received port using an UDP socket a message. The server should received the message and returned it reversed.

## Compile/run the program
To run the program first it is necessary to run the server.py file using the terminal using the following format for the command:

    > python server.py <n_port> <req_code>

Where the 2 required arguments are the following:
 - n_port is the port used to negotitate using TCP.
 - req_code is an integer wich indicates the code to stablish the UDP connection.

When the server.py is running then it is needed to run the client.py file using also the terminal with the following command:

    > python client.py <server_address> <n_port> <req_code> <msg>

Where the 4 required arguments are the following:
 -  server_address is the direction of the server to send the message.
 - n_port is the port used to negotitate using TCP.
 - req_code is an integer wich indicates the code to stablish the UDP connection.
 - msg is the text to be reversed.
