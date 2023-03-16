import os, time
import vlc
import platform
import tkinter as tk
import random

class Musicplayer():

    def __init__(self, *args):

        #self._songlist = []
        # read list of songs
        filepath = 'songlist//'
        self._songlist = os.listdir(filepath)
        self._pathlist = [filepath + i for i in self._songlist]
        self._ord_ID = 0    
        self._volume = 50

        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()




    # Methods

    # set url
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # play a song
    def playmusic(self, path=None):
        self.set_uri(self._pathlist[self._ord_ID])
        return self.media.play()

    # pause a song
    def pausemusic(self):
        self.media.pause()

    # resume
    def resume(self):
        self.media.set_pause(0)


    # get the current state
    # (1 - playing; 0 - not playing, -1 - otherwise)
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # get current songname
    def get_song(self):
        return self._songlist[self._ord_ID]

    # skip the current song
    def playnext(self):
        self._ord_ID = self._ord_ID + 1
        if self._ord_ID >= len(self._songlist):
            self._ord_ID = 0
        
        self.set_uri(self._pathlist[self._ord_ID])
        return self.media.play()


    # play the previous song
    def playprev(self):
        self._ord_ID = self._ord_ID - 1
        if self._ord_ID < 0:
            self._ord_ID = len(self._songlist) - 1
        
        self.set_uri(self._pathlist[self._ord_ID])
        return self.media.play()

    # play the selected song
    def playselected(self, selection):
        self._ord_ID = selection
        self.set_uri(self._pathlist[self._ord_ID])
        return self.media.play()

    # set window
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.media.set_hwnd(wm_id)
        else:
            self.media.set_xwindow(wm_id)

    # register callback
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # remove callback
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)

    # set volume
    def set_volume(self, volume):
        self._volume = volume
        self.media.audio_set_volume(volume)

    # volume up
    def volume_up(self):
        self._volume = self._volume + 10
        self.media.audio_set_volume(self._volume)

    # volume down
    def volume_down(self):
        self._volume = self._volume - 10
        self.media.audio_set_volume(self._volume)
        
    # get current volume
    def get_current_volume(self):
        return self._volume

    # get current music progress
    def current_position(self):
        return self.media.get_time()

    # get total time of the song
    def get_length(self):
        return self.media.get_length()

    # shuffle the current playlist
    def shuffle_playlist(self):
        # the songlist and the pathlist should be in same order
        zip_list = list(zip(self._songlist, self._pathlist))
        random.shuffle(zip_list)
        self._songlist, self._pathlist = zip(*zip_list)
        self._songlist = list(self._songlist)
        self._pathlist = list(self._pathlist)


    
