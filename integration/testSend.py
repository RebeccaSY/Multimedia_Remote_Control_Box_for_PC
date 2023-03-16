from socket import *
import sys

if (len(sys.argv) != 2):
    print ("Usage: python3 testSend.py serverPortNo")
    sys.exit()

server_port = int(sys.argv[1])
print(f"port no = {server_port}")


while True:
    signal = input("Enter a signal: ")
    # Making the socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('127.0.0.1', server_port))
    clientSocket.send(signal.encode('utf-8'))
    # Close the socket
    clientSocket.close()