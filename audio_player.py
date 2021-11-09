import tkinter as tk
import glob
import pygame
import threading


def f_files():
    a_list = glob.glob('./*.mp3')
    return a_list


class AudioPlayer:
    curr_index = 0
    audio_list = list()
    new_song = True
    playing = False
    game = pygame
    mix = game.mixer
    song_pos = 0.0
    repeat = False
    SONG_END = pygame.USEREVENT + 1
    next_clicked = False
    start_state = True

    def full_stop_music(self):
        self.mix.music.stop()
        self.playing = False
        self.new_song = True
        self.curr_index = 0
        self.btn_play.config(text="play")

    def stop_music(self):
        self.mix.music.stop()
        self.playing = False

    def prev_song(self):
        self.start_state = True
        if self.playing:
            if self.curr_index != 0:
                self.curr_index -= 1
            else:
                self.curr_index = len(self.audio_list) - 1
            self.new_song = True
            self.stop_music()
            self.playing = False
            self.play_music()
        else:
            if self.curr_index != 0:
                self.curr_index -= 1
            else:
                self.curr_index = len(self.audio_list) - 1
        self.start_state = False
        # print(self.curr_index)

    def next_song(self):
        self.start_state = True
        if self.playing:
            if self.curr_index == len(self.audio_list) - 1:
                self.curr_index = 0
            else:
                self.curr_index += 1
            self.new_song = True
            self.stop_music()
            self.play_music()
        else:
            if self.curr_index == len(self.audio_list) - 1:
                self.curr_index = 0
            else:
                self.curr_index += 1
        self.start_state = False
        # print(self.curr_index)

    def play_music(self):
        if self.playing:
            self.mix.music.pause()
            self.song_pos = self.mix.music.get_pos()
            self.btn_play.config(text="play")
            self.playing = False
        else:
            if self.repeat:
                temp_repeat = -1
            else:
                temp_repeat = 1
            match self.new_song:
                case False:
                    if self.song_pos == 0:
                        self.mix.music.play()
                        self.btn_play.config(text="pause")
                        self.playing = True
                    else:
                        self.mix.music.unpause()
                        self.btn_play.config(text="pause")
                        self.playing = True
                    self.start_state = False
                case True:
                    self.mix.music.load(self.audio_list[self.curr_index])
                    song_name: str = self.audio_list[self.curr_index]
                    new_s_name = song_name.replace(".\\", "")
                    self.curr_song.config(text=new_s_name)
                    self.mix.music.play(loops=temp_repeat)
                    self.btn_play.config(text="pause")
                    self.new_song = False
                    self.playing = True
                    self.start_state = False

    def change_vol(self, value):
        self.mix.music.set_volume(float(value) / 100)

    def change_repeat(self):
        if self.repeat:
            self.btn_repeat.config(text="repeat off")
            self.repeat = False
        else:
            self.btn_repeat.config(text="repeat on")
            self.repeat = True

    def check_music(self):
        while True:
            for event in self.game.event.get():
                if event.type == self.SONG_END & self.start_state == False:
                    print("smth")
                    self.next_song()

    def __init__(self):
        self.window = tk.Tk(className="Player")
        self.window.resizable(False, False)
        self.audio_list = f_files()

        self.game.init()
        self.mix.init()

        self.window.rowconfigure([0, 1], minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)

        self.btn_prev = tk.Button(master=self.window, text="<")
        self.btn_prev.config(command=self.prev_song)
        self.btn_prev.grid(row=0, column=0, sticky="nsew")

        self.btn_play = tk.Button(master=self.window, text="play")
        self.btn_play.config(command=self.play_music)
        self.btn_play.grid(row=0, column=1, sticky="nsew")

        self.btn_next = tk.Button(master=self.window, text=">")
        self.btn_next.config(command=self.next_song)
        self.btn_next.grid(row=0, column=2, sticky="nsew")

        self.btn_stop = tk.Button(master=self.window, text="stop")
        self.btn_stop.config(command=self.full_stop_music)
        self.btn_stop.grid(row=0, column=3, sticky="nsew")

        self.btn_repeat = tk.Button(master=self.window, text="repeat off")
        self.btn_repeat.config(command=self.change_repeat)
        self.btn_repeat.grid(row=0, column=4, sticky="nsew")

        self.curr_song = tk.Label(master=self.window, text="Current song")
        self.curr_song.grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.scale = tk.Scale(from_=100, to=0, command=self.change_vol)
        self.scale.grid(row=0, rowspan=2, column=5, sticky="nsew")
        self.scale.set(50)

        self.mix.music.set_endevent(self.SONG_END)

        self.check_thread = threading.Thread(target=self.check_music, daemon=True)
        self.check_thread.start()

        self.window.mainloop()
