# COMP3601: Design Project A
# This receives the inputs from the fpga via a socket
# from a C++ program
# Usage "python3 fpgaRecv.py server_port"
# Usuall done in "python3 fpgaRecv.py 8888"

from socket import *
import sys

if (len(sys.argv) != 2):
    print ("Usage: python3 fpgaRecv.py serverPortNo")
    sys.exit()

server_port = int(sys.argv[1])
print(f"port no = {server_port}")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', server_port))
server_socket.listen(5)

print("The server is ready to receive")
prev_vol = 0


while True:
    conn_socket, addr = server_socket.accept()
    message = conn_socket.recv(1024).decode('utf-8')
    print(f"recv message = {message}")
    # extracting first 5 bits
    vol_recv = int(message)
    vol_recv = (vol_recv >> 3) & (31)

    # extract last 3 bits
    inst_out = int(message)
    inst_out = (inst_out & 7)

    # parsing the data so that it only outputs to program on important info
    if (vol_recv == prev_vol and inst_out == 0):
        print("ignored data")
    elif (vol_recv != prev_vol and inst_out == 0):
        prev_vol = vol_recv
        print(f"replace this print with change_vol({vol_recv})")
    elif (vol_recv == prev_vol and inst_out != 0):
        print(f"replace this print with do_command({inst_out})")
    else:
        print("should not get here!")
    #print(f"vol_recv = {vol_recv} and inst_out = {inst_out}")
    conn_socket.close()

