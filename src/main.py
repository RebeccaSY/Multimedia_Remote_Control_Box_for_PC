import os, time
import vlc
import platform
import tkinter as tk

from view import View
from musicplayer import Musicplayer

import threading 
from socket import *

def socket_thread():
    global mp
    global server_socket
    global view
    
    print("Server is ready to recv...")
    while True:
        conn_socket, addr = server_socket.accept()
        msg = conn_socket.recv(1024).decode('utf-8')
        print(f"recv message = {msg}")

        # extracting the first 5 bits
        vol_recv = int(msg)
        vol_recv = (vol_recv >> 3) & (31)

         # extract last 3 bits
        inst_out = int(msg)
        inst_out = (inst_out & 7)

        prev_vol = 0
        # parsing the data so that it only outputs to program on important info
        if (vol_recv == prev_vol and inst_out == 0):
            print("ignored data")
        elif (vol_recv != prev_vol and inst_out == 0):
            prev_vol = vol_recv
            print(f"replace this print with change_vol({vol_recv})")
            mp.set_volume(vol_recv)

        elif (vol_recv != prev_vol and inst_out == 1):
            # start up
            print(f"1")
        elif (vol_recv == prev_vol and inst_out == 2):
            # need a condition checking if the current song is paused
            print(f"replace this print with play({inst_out})")
            if mp.get_state() == 0:
                mp.resume()
            elif mp.get_state() == 1:
                pass  
            else:
                mp.playmusic()
        
            # player.resume()
        elif (vol_recv == prev_vol and inst_out == 3):
            print(f"replace this print with pause({inst_out})")
            print("Pausing music ...")
            mp.pausemusic()
        elif (vol_recv == prev_vol and inst_out == 4):
            print(f"replace this print with skip({inst_out})")
            mp.playnext()
            view.update_song_name()
        elif (vol_recv == prev_vol and inst_out == 5):
            print(f"replace this print with prev({inst_out})")
            mp.playprev()
            view.update_song_name()

        else:
            print("should not get here!")
        conn_socket.close()




if "__main__" == __name__:
    # Making the music player
    mp = Musicplayer()
    view = View(mp)

    # Making the socket stuff
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(5)
    

    socket_th = threading.Thread(name='Socket_Thread', target=socket_thread)
    socket_th.daemon = True

    socket_th.start()

    view.mainloop()


    while True:
        time.sleep(0.1)

