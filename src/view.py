import os, time
import vlc
import platform
from tkinter.filedialog import askopenfilename
import tkinter as tk
from tkinter import *
from tkinter import ttk
from musicplayer import Musicplayer
import random
import socket


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


class View(tk.Tk):

    def __init__(self, musicplayer):
        super().__init__()
        self.musicplayer = musicplayer
        self.title("MusicPlayer")
        self.configure(background='DarkSlateBlue')
        self.geometry('800x420')
        self._songname = self.musicplayer.get_song()
        self._volume = 50
        self._progress = 0
        self.play()
        self.pause()
        #self.create_bg_view()
        self.create_title()         # create title
        self.create_listbox()       # the playlist
        self.create_listbuttons()   # "Add song" & "Delete song"
        self.create_volume_view()   # "+" or "-" volume
        self.create_control_view()  # "PLAY", "PAUSE", "PREV" ... ...
        self.create_progressbar()   # progress of current song
        self.create_label()         # show current song name
        # self.connect()
        # self.update_progress()
        # self.playprev()
        # self.pause()


    # create the background
    def create_bg_view(self):
        self._canvas = tk.Canvas(self, bg="black", width=800, height=420)
        self._canvas.pack()
        self.musicplayer.set_window(self._canvas.winfo_id())
    
    # show current song name
    def create_label(self):
        self._label = tk.Label(self, text=self._songname, font=('Arial', 12), fg='Seashell', bg='DarkSlateBlue')
        self._label.pack(side=BOTTOM)
    
    # create title
    def create_title(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        tk.Label(frame, text="PLAYLIST", font=('Arial', 12, 'bold'), fg='Seashell', bg='DarkSlateBlue').pack(side=LEFT)
        tk.Label(frame, text="(double click to play a selected song)", font=('Arial', 9), fg='Seashell', bg='DarkSlateBlue').pack(side=LEFT)
        frame.pack(side=TOP, padx=80, pady=10)

    # the playlist
    def create_listbox(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        self._listbox = tk.Listbox(frame, width=500, selectbackground='PowderBlue')
        
        list_scroll = tk.Scrollbar(frame, orient=VERTICAL)  
        list_scroll.pack(side=RIGHT, fill=Y)
        self._listbox['yscrollcommand'] = list_scroll.set
        list_scroll.config(command=self._listbox.yview)

        for song in self.musicplayer._songlist:
            self._listbox.insert("end", song)
        
        self._listbox.bind('<Double-1>', self.double_click)
        self._listbox.pack()
        frame.pack(side=TOP, padx=80, pady=3)

    # "Add song" & "Delete song"
    def create_listbuttons(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        tk.Button(frame, text="Add song", width=15, height=1, command=self.browse_local_file).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="Delete song", width=15, height=1, command=self.delete_song).pack(side=tk.LEFT, padx=10)
        frame.pack(side=TOP)

    # "PLAY", "PAUSE", "PREV" ... ...
    def create_control_view(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        tk.Button(frame, text="PLAY", command=lambda: self.click(0)).pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="PAUSE", command=lambda: self.click(1)).pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="SKIP", command=lambda: self.click(2)).pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="PREV", command=lambda: self.click(3)).pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="REPEAT", command=lambda: self.click(4)).pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="RANDOM", command=lambda: self.click(7)).pack(side=tk.LEFT, padx=7)
        frame.pack(side=BOTTOM, pady=2)

    # "+" or "-" volume
    def create_volume_view(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        tk.Button(frame, text="+", width=2, height=1, command=lambda: self.click(5)).pack(side=tk.LEFT, padx=7)
        self._vol = tk.StringVar()
        self._vol.set(self.musicplayer.get_current_volume())
        self._volLabel = tk.Label(frame, textvariable=self._vol, font='Arial', fg='Seashell', bg='DarkSlateBlue').pack(side=tk.LEFT, padx=7)
        tk.Button(frame, text="-", width=2, height=1, command=lambda: self.click(6)).pack(side=tk.LEFT, padx=7)
        frame.pack(side=BOTTOM, pady=10)

    # progress of current song
    def create_progressbar(self):
        frame = tk.Frame(self, bg='DarkSlateBlue')
        self.music_progress = tk.StringVar()

        # Playback progress bar
        self.progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=500)
        self.progress_bar.pack(side=tk.LEFT, padx=7)
        
        pos_time = self.musicplayer.current_position()
        self._posText = tk.StringVar()
        self._posText.set(self.format_duration(pos_time))
        self._lbTime = tk.Label(frame, textvariable=self._posText, font='Arial', fg='Seashell', bg='DarkSlateBlue').pack(side=tk.LEFT, padx=1)
        tk.Label(frame, text="/", font='Arial', fg='Seashell', bg='DarkSlateBlue').pack(side=tk.LEFT, padx=1)
        total_time = self.musicplayer.get_length()
        self._timeText = tk.StringVar()
        self._timeText.set(self.format_duration(total_time))
        self._lbLength = tk.Label(frame, textvariable=self._timeText, font='Arial', fg='Seashell', bg='DarkSlateBlue').pack(side=tk.LEFT, padx=1)
        
        frame.pack(side=BOTTOM, pady=2)


    def click(self, action):
        if action == 0:
            # play music
            self.play()
        elif action == 1:
            # pause music
            self.pause()
        elif action == 2:
            # play next music
            self.playnext()
        elif action == 3:
            # play prev music
            self.playprev()
        elif action == 4:
            # repeat
            self.musicplayer.playmusic()
        elif action == 7:
            # shuffle playlist
            self.shuffle_playlist()


        elif action == 5:
            # volume up
            if self.musicplayer.get_current_volume() <= 90:
                self.musicplayer.volume_up()
            self._vol.set(self.musicplayer.get_current_volume())

        elif action == 6:
            # volume down
            if self.musicplayer.get_current_volume() >= 10:
                self.musicplayer.volume_down()
            self._vol.set(self.musicplayer.get_current_volume())

        # elif action == 7:
        #     print("hello there")
        
        #self.receive_msg()
        self.update_progress()

    # play the selected song when double-clicked
    def double_click(self, event):
        selected = self._listbox.curselection()
        selection = int(selected[0])
        self.musicplayer.playselected(selection)
        self.update_song_name()
        self.update_progress()

    # display the time in minutes and seconds
    def format_duration(self, ms):
        total_s = ms / 1000
        total_min = total_s / 60
        remain_s = total_s % 60
        return ('%02d:%02d' % (total_min, remain_s))

    # update the progress of the current song
    def update_progress(self):
        pos_ms = self.musicplayer.current_position()
        total_ms = self.musicplayer.get_length()
        if(total_ms == 0): 
            return
        progress_percent = pos_ms / float(total_ms) * 100
        # print(progress_percent)
        # Update the progress bar
        self.progress_bar["value"] = progress_percent
        # When a song ends, play the next
        if pos_ms + 200 > total_ms:
            self.click(2)
        self._posText.set(self.format_duration(pos_ms))
        self._timeText.set(self.format_duration(total_ms))

        # Schedule next update in 100ms        
        self.after(1000, self.update_progress)


    def shuffle_playlist(self):
        num_songs = len(self.musicplayer._songlist)
        #for index in range(0, num_songs - 1):
        #    self._listbox.delete(index)
        self._listbox.delete(first=0, last=num_songs-1)
        self.musicplayer.shuffle_playlist()

        for song in self.musicplayer._songlist:
            self._listbox.insert("end", song)
        self.playnext()
    

    def play(self):
        if self.musicplayer.get_state() == 0:
            self.musicplayer.resume()
        elif self.musicplayer.get_state() == 1:
            pass  
        else:
            self.musicplayer.playmusic()
        # self.update_progress()

    def pause(self):
        if self.musicplayer.get_state() == 1:
            self.musicplayer.pausemusic()

    def playnext(self):
        self.musicplayer.playnext()
        self.update_song_name()
        self.update_progress()

    def playprev(self):
        self.musicplayer.playprev()
        self.update_song_name()
        self.update_progress()

    # update the song name on label
    def update_song_name(self):
        self._songname = self.musicplayer.get_song()
        self._label["text"] = self._songname    

    # browse to add song
    def browse_local_file(self):
        file_selected = askopenfilename()
        file_name = os.path.basename(file_selected)
        self._listbox.insert(len(self.musicplayer._songlist), file_name)
        self.musicplayer._songlist.append(file_name)
        self.musicplayer._pathlist.append(file_selected)

    # delete the selected song
    def delete_song(self):
        selected = self._listbox.curselection()
        selected = int(selected[0])
        self._listbox.delete(selected)
        if(selected == self.musicplayer.get_song):
            self.next()
        del self.musicplayer._songlist[selected]
        del self.musicplayer._pathlist[selected]


    # def connect(self):
    #     # try:
    #     s.bind(('127.0.0.1', (8888)))
    #     s.listen(5)
    #     print("Server is ready")
    #     # s.connect('127.0.0.1', (8888))

    #     #Receive messages
    #     # self.receive_msg()
    #     # except:
    #     #     print("Start server failed")

    # def receive_msg(self):
    #     #Prepared to receive message
    #     print("Preparing to receive")
    #     conn_socket, addr = s.accept()
    #     message = conn_socket.recv(1024).decode('utf-8')
    #     print(f"recv message = {message}")
    #     # extracting first 5 bits
    #     vol_recv = int(message)
    #     vol_recv = (vol_recv >> 3) & (31)

    #     # extract last 3 bits
    #     inst_out = int(message)
    #     inst_out = (inst_out & 7)

    #     prev_vol = 0
    #     # parsing the data so that it only outputs to program on important info
    #     if (vol_recv == prev_vol and inst_out == 0):
    #         print("ignored data")
    #     elif (vol_recv != prev_vol and inst_out == 0):
    #         prev_vol = vol_recv
    #         print(f"replace this print with change_vol({vol_recv})")
            
    #     elif (vol_recv != prev_vol and inst_out == 1):
    #         # start up
    #         print(f"replace this print with start({vol_recv})")

    #     elif (vol_recv == prev_vol and inst_out == 2):
    #         # need a condition checking if the current song is paused
    #         print(f"replace this print with play({inst_out})")
    #         # player.resume()
    #     elif (vol_recv == prev_vol and inst_out == 3):
    #         print(f"replace this print with pause({inst_out})")
    #     elif (vol_recv == prev_vol and inst_out == 4):
    #         print(f"replace this print with skip({inst_out})")
    #     elif (vol_recv == prev_vol and inst_out == 5):
    #         print(f"replace this print with prev({inst_out})")
    #     else:
    #         print("should not get here!")
    #     conn_socket.close()
    #     self.click(inst_out - 2)
