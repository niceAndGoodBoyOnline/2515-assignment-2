import tkinter as tk
from tkinter import Scrollbar


class PlaylistsWindow(tk.Frame):
    """ Layout for the Chooser Window """

    def __init__(self, parent, load_callback, desc_callback, delete_callback, close_callback):
        """ init playlists window """
        tk.Frame.__init__(self, parent)
        self._load = load_callback
        self._description = desc_callback
        self._delete = delete_callback
        self._close = close_callback

        parent.title('Playlists')
        parent.lift()

        # Frames
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0)

        self.bot_frame = tk.Frame(self.master)
        self.bot_frame.grid(row=1)

        # playlists box
        self.playlists_box = tk.Listbox(self.top_frame, width=20, height=10)
        self.playlists_box.grid(row=0, column=0)
        self.playlists_box.config(width=50)

        # Vertical Scrollbar
        v_scrollbar = Scrollbar(self.top_frame, orient="vertical", width=20)
        v_scrollbar.config(command=self.playlists_box.yview)
        v_scrollbar.grid(row=0, column=1, sticky="NS")

        self.playlists_box.config(yscrollcommand=v_scrollbar.set)

        self.load = tk.Button(self.bot_frame, text='Load', width=10, command=self._load)
        self.load.grid(row=0, column=0)

        self.description = tk.Button(self.bot_frame, text="Description", command=self._description)
        self.description.grid(row=0, column=1)

        self.delete = tk.Button(self.bot_frame, text="Delete Playlist", command=self._delete)
        self.delete.grid(row=0, column=2)

        self.close = tk.Button(self.bot_frame, text='Close', width=10, command=self._close)
        self.close.grid(row=0, column=3)

    def set_playlist_songs(self, songs):
        """ refresh playlist songs """
        self.playlists_box.delete(0, tk.END)
        for song in songs:
            self.playlists_box.insert(tk.END, song)

    def get_playlist_info(self):
        """ returns playlist name in json """
        try:
            playlist_name = self.playlists_box.get(self.playlists_box.curselection())
            print(playlist_name)
            return {"playlist_name":playlist_name}
        except Exception as e:
            print(e)