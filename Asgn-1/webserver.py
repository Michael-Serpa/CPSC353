# Web Server Lab - CPSC 353 Networks
# Student: [Your Name Here]
# Date: [Date]

# Import socket module
from socket import *
import sys  # In order to terminate the program

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Fill in start - Bind the socket to server address and server port
# Hint: You need to bind the socket to a specific address and port
# Use serverSocket.bind() method
serverSocket.bind(('localhost', 6789))  # Bind to localhost on port 6789
# Fill in end

# Fill in start - Configure the socket to listen for incoming connections
# Hint: Use serverSocket.listen() method with appropriate backlog
serverSocket.listen(1)  # Allow 1 pending connection
# Fill in end

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # Receive the HTTP request and decode it
        raw = connectionSocket.recv(1024)     # bytes from client
        message = raw.decode()                 # convert to str
        
        # Extract the filename from the HTTP request
        filename = message.split()[1]
        
        # Open the requested file
        f = open(filename[1:])  # Remove the leading '/' from filename
        
        # Read the content of the file
        outputdata = f.read()

        
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(outputdata.encode())}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        connectionSocket.send(header.encode())
        
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        # Close the file
        f.close()
        connectionSocket.close()
        
    except IOError:
        # Send response message for file not found (404 error)
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        connectionSocket.sendall(header.encode() + body.encode())

        # Close client socket
        connectionSocket.close()


# Close server socket and terminate program
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
