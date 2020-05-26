import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from tkinter.filedialog import askopenfilename
import os
from tkinter import Scrollbar


class PlayerWindow(tk.Frame):
    """ Layout for the Player Window """

    def __init__(self, parent, controller):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        # 1: create any instances of other support classes that are needed
        parent.title('cool dumb media player')
        parent.geometry('1600x900')
        parent.resizable(False, False)
        parent.wm_attributes("-topmost", False)
        self.controller = controller
        self.window = parent
        # UI assets & settings
        self.state = True
        ui = os.getcwd() + "/ui/"
        self.play_icon = tk.PhotoImage(file = ui + "play.png")
        exit_icon = tk.PhotoImage(file = ui + 'exit.png')
        self.pause_icon = tk.PhotoImage(file = ui + "pause.png")
        folder_image = tk.PhotoImage(file = ui + 'folder64.png')
        ff_icon = tk.PhotoImage(file = ui + "ff.png")
        rw_icon = tk.PhotoImage(file = ui + "rw.png")
        bg_img = tk.PhotoImage(file = ui + "bg.png")
        background = tk.Label(parent, image=bg_img)
        background.photo = bg_img
        background.place(x=0, y=0, relwidth=1, relheight=1)
        self._player_target_bool = tk.BooleanVar()

        BOX_WIDTH = 1200
        BOX_HEIGHT = 400
        RIGHT_WIDTH = 380
        RIGHT_HEIGHT = 410
        OPT_WIDTH = 27
        OPT_HEIGHT = 35

        # library
        library_frame = tk.Frame(master=background, width=BOX_WIDTH, height=BOX_HEIGHT)
        library_frame.columnconfigure(0,weight=10)
        library_frame.place(x=20,y=20)


        self.library = tk.Listbox(library_frame)
        self.library.place(x=0,y=0, width=BOX_WIDTH,height=BOX_HEIGHT)

        v_scrollbar = Scrollbar(library_frame, orient="vertical")
        v_scrollbar.config(command=self.library.yview)
        v_scrollbar.place(x=(BOX_WIDTH-20), y=0, width=20, height=BOX_HEIGHT)
        self.library.config(yscrollcommand=v_scrollbar.set)

        # feedback
        self.feedback_frame = tk.Frame(master=background,width=BOX_WIDTH,height=32)
        self.feedback_frame.columnconfigure(0,weight=10)
        self.feedback_frame.place(x=20,y=440)

        self.feedback = tk.Label(self.feedback_frame, anchor=tk.NW, text="user feedback shows up here!")
        self.feedback.place(x=0,y=0)

        # playlist functinality
        playlist_frame = tk.Frame(master=background, width=BOX_WIDTH, height=BOX_HEIGHT)
        playlist_frame.columnconfigure(0,weight=10)
        playlist_frame.place(x=20, y=(BOX_HEIGHT+90))

        self.playlist= tk.Listbox(playlist_frame)
        self.playlist.place(x=0,y=0, width=BOX_WIDTH, height=BOX_HEIGHT)

        v_scrollbar2 = Scrollbar(playlist_frame, orient="vertical", width=20)
        v_scrollbar2.config(command=self.playlist.yview)
        v_scrollbar2.place(x=(BOX_WIDTH-20), y=0, width=20, height=BOX_HEIGHT)
        self.playlist.config(yscrollcommand=v_scrollbar2.set)

        # Library/Playlist functinality
        options_options = dict(font=font.Font(size=7),
                                bd=0, relief=tk.GROOVE
                                )

        options_frame = tk.Frame(master=background, bg="darkgrey", width=(RIGHT_WIDTH-40), height=(RIGHT_HEIGHT -30) )
        options_frame.place(x=(BOX_WIDTH+40),y=20)

        add_file_button = tk.Button(options_frame,text='Add File',anchor=tk.W, width=(OPT_WIDTH//2),**options_options, command=controller.add_from_file_callback, )
        add_file_button.place(x=0,y=0)
        

        tk.Button(options_frame, text='Add URL', anchor=tk.W, width=(OPT_WIDTH//2),**options_options, command=controller.open_url_callback) \
                .place(x=150,y=0)

        tk.Button(options_frame, text='Edit Meta Data', anchor=tk.W, width=OPT_WIDTH,**options_options, command=controller.open_edit_metadata_callback) \
                .place(x=0,y=1*OPT_HEIGHT)

        folder_button = tk.Button(options_frame, image=folder_image, anchor=tk.W, bg="darkgrey",command=controller.add_music_folder)
        folder_button.place(x=270,y=0)
        folder_button.photo = folder_image

        tk.Button(options_frame, text='Remove From Library',anchor=tk.W, width=OPT_WIDTH,**options_options, command=controller.delete_callback) \
                .place(x=0,y=2*OPT_HEIGHT)

        tk.Button(options_frame, text='Filter Library',anchor=tk.W, width=OPT_WIDTH, **options_options, command=controller.open_filter_library_callback) \
                .place(x=0,y=3*OPT_HEIGHT)  

        tk.Button(options_frame, text='New Playlist',anchor=tk.W, width=OPT_WIDTH, **options_options, command=controller.open_new_playlist_callback) \
                .place(x=0,y=4*OPT_HEIGHT)

        tk.Button(options_frame, text='Playlists',anchor=tk.W, width=OPT_WIDTH, **options_options, command=controller.open_playlists_callback) \
                .place(x=0,y=5*OPT_HEIGHT) 

        tk.Button(options_frame, text='Add to Playlist',anchor=tk.W, width=OPT_WIDTH,**options_options,  command=controller.add_song_to_playlist_callback) \
                .place(x=0,y=6*OPT_HEIGHT)  

        tk.Button(options_frame, text='Remove From Playlist',anchor=tk.W, width=OPT_WIDTH, **options_options, command=controller.delete_song_from_playlist_callback) \
                .place(x=150,y=6*OPT_HEIGHT) 

        # Playlist Name Area

        playlist_name_display_frame = tk.Frame(master=background, width=340, height=100)
        playlist_name_display_frame.place(x=(BOX_WIDTH+40), y=(BOX_HEIGHT+20))

        self.playlist_display_head = tk.Label(playlist_name_display_frame, anchor=tk.NW, font=font.Font(size=7), text="Current Playlist")
        self.playlist_display_head.place(x=0,y=0)

        self.playlist_name_label = tk.Label(playlist_name_display_frame,font=font.Font(size=20), anchor=tk.W, text="")
        self.playlist_name_label.place(x=0,y=30)

    
        # VLC functionality
        player_frame = tk.Frame(master=background, bg="darkgrey", width=256, height=256)
        player_frame.place(x=(BOX_WIDTH+90),y=(BOX_HEIGHT+150))
        # player_frame.grid(row=2, column=1, padx=80,pady=3)
        # player_frame.columnconfigure(0,weight=10)
        # player_frame.grid_propagate(False)

        self.play_button = tk.Button(player_frame, image=self.play_icon, command=controller.play_callback, bg="darkgrey",bd=0)
        self.play_button.photo = self.play_icon
        self.play_button.place(x=0,y=0)
        # self.play_button.grid(row=0, column=0, sticky=tk.E)

        exit_button = tk.Button(player_frame, image=exit_icon,command=controller.quit_callback, bg="darkgrey",bd=0)
        exit_button.photo = exit_icon
        exit_button.place(x=128,y=0)
        # exit_button.grid(row=0, column=1)

        rw_button = tk.Button(player_frame, image=rw_icon, command=controller.play_previous_callback, bg="darkgrey",bd=0)
        rw_button.photo = rw_icon
        rw_button.place(x=0,y=128)
        # rw_button.grid(row=1, column=0, sticky=tk.E,)

        ff_button = tk.Button(player_frame, image=ff_icon, command=controller.play_next_callback, bg="darkgrey", bd=0)
        ff_button.photo = ff_icon
        ff_button.place(x=128,y=128)
        # ff_button.grid(row=1, column=1, sticky=tk.E)

        player_target_frame = tk.Frame(master=background, bg="darkgrey", width=258, height=32)
        player_target_frame.place(x=(BOX_WIDTH-239),y=440)

        self.player_target = tk.Checkbutton(player_target_frame, bg='darkgrey', bd=0, text="Playing from Library", font=font.Font(size=8), variable=self._player_target_bool, onvalue=True, offvalue=False, command=self.swap_player_target)
        self.player_target.place(x=0,y=0)

        playlist_label_frame = tk.Frame(master=background, width=160, height=36)
        playlist_label_frame.place(x=1040,y=853)

        playlist_label = tk.Label(playlist_label_frame, font=font.Font(size=12),text='PLAYLIST')
        playlist_label.place(x=0,y=0)

        library_label_frame = tk.Frame(master=background, width=145, height=36)
        library_label_frame.place(x=1055,y=382)

        library_label = tk.Label(library_label_frame, font=font.Font(size=12),text='LIBRARY')
        library_label.place(x=0,y=0)

    def set_library_songs(self, songs: list):
        """ sets songs intolibrary """
        self.library.delete(0, tk.END)
        for song in songs:
            self.library.insert(tk.END, song)

    def get_playlist_songs(self):
        """ gets list from playlist box """
        size = self.playlist.size() - 1
        return self.playlist.get(0,size)

    def set_playlist_songs(self, songs: list):
        """ sets songs into playlist """
        self.playlist.delete(0, tk.END)
        for song in songs:
            self.playlist.insert(tk.END, song)

    def set_playlist_name(self, playlist_name: str):
        """ set the playlist name """
        print(playlist_name)
        self.playlist_name_label.config(text=playlist_name)

    def set_info(self, update: str):
        """ updates the info label """
        self.feedback_frame.config(bg='red')
        self.feedback.config(text=update)
        self.after(500, self.feedback_frame.config(bg='lightgrey'))


    def set_icon(self, status: bool):
        """ changes between play and pause icons """
        if status:
            self.play_button.config(image=self.play_icon)
            self.play_button.photo = self.play_icon
        else:
            self.play_button.config(image=self.pause_icon)
            self.play_button.photo = self.pause_icon

    def swap_player_target(self):
        """ changes player target """
        if self._player_target_bool.get():
            self.player_target.config(text="Playing From Library")
            self.play_button.config(command=self.controller.play_callback)
        else:
            self.player_target.config(text="Playing From Playlist")
            self.play_button.config(command=self.controller.play_playlist_callback)

    def toggle_window_depth(self):
        """ lift/lower main window when it improves UX """
        if self.state:
            self.state = False
            self.window.lower()
        else:
            self.state = True
            self.window.lift()