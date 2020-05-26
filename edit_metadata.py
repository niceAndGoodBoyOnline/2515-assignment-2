import tkinter as tk
from typing import Dict


class EditMetadata(tk.Frame):
    """ Layout for the Chooser Window """

    def __init__(self, parent, commit_callback, close_callback, song_data):
        """ Initialize the popup listbox window """
        tk.Frame.__init__(self, parent)
        self._commit = commit_callback
        self._close = close_callback
        self._current_metadata = song_data
        parent.title('Edit Metadata')

        # Frames
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=0)

        self.bot_frame = tk.Frame(self.master)
        self.bot_frame.grid(row=1, padx=30, pady=0)

        # Labels and entries

        self._title_label = tk.Label(self.top_frame, text='Title:')
        self._title_label.grid(row=0, column=0, sticky=tk.N)

        self._title_entry = tk.Entry(self.top_frame, width=40)
        self._title_entry.grid(row=0, column=1, sticky=tk.N)

        self._artist_label = tk.Label(self.top_frame, text='Artist:')
        self._artist_label.grid(row=1, column=0, sticky=tk.N)

        self._artist_entry = tk.Entry(self.top_frame, width=40)
        self._artist_entry.grid(row=1, column=1, sticky=tk.N)

        self._album_label = tk.Label(self.top_frame, text='Album:')
        self._album_label.grid(row=2, column=0, sticky=tk.N)

        self._album_entry = tk.Entry(self.top_frame, width=40)
        self._album_entry.grid(row=2, column=1, sticky=tk.N)

        self._genre_label = tk.Label(self.top_frame, text='Genre:')
        self._genre_label.grid(row=3, column=0, sticky=tk.N)

        self._genre_entry = tk.Entry(self.top_frame, width=40)
        self._genre_entry.grid(row=3, column=1, sticky=tk.N)

        self._rating_label = tk.Label(self.top_frame, text='Rating:')
        self._rating_label.grid(row=4, column=0, sticky=tk.N)

        self._rating_entry = tk.Entry(self.top_frame, width=40)
        self._rating_entry.grid(row=4, column=1, sticky=tk.N)

        # Buttons
        self.save_button = tk.Button(self.bot_frame, text='Save', width=10)
        self.save_button.grid(row=0)
        self.save_button.bind("<Button-1>", self._commit)

        self.save_button = tk.Button(self.bot_frame, text='Reset', width=10)
        self.save_button.grid(row=0, column=1)
        self.save_button.bind("<Button-1>", self.revert_metadata)

        self.cancel_button = tk.Button(self.bot_frame, text='Cancel', width=10)
        self.cancel_button.grid(row=0, column=2)
        self.cancel_button.bind("<Button-1>", self._close)

    def get_new_metadata(self):
        """ grabs info from entry and returns nested json"""
        return {
                "old":self._current_metadata,
                "new":{"title":self._title_entry.get(), 
                "artist":self._artist_entry.get(),
                "album":self._album_entry.get(),
                "genre":self._genre_entry.get(),
                "rating":self._rating_entry.get()
                }
        }

    def revert_metadata(self,event):
        """ resets the entry fields to those of self._current_metadata"""
        self._title_entry.delete(0, tk.END)
        self._artist_entry.delete(0, tk.END)
        self._album_entry.delete(0, tk.END)
        self._genre_entry.delete(0, tk.END)
        self._rating_entry.delete(0, tk.END)
        self.set_metadata()

    def set_metadata(self):
        """ puts the old metadata into the entry fields, for better UX """
        self._title_entry.insert(tk.END, self._current_metadata['title'])
        self._artist_entry.insert(tk.END, self._current_metadata['artist'])
        self._album_entry.insert(tk.END, self._current_metadata['album'])
        try:
            if type(self._current_metadata['rating']) is int:
                self._rating_entry.insert(tk.END, self._current_metadata['rating'])
            if len(self._current_metadata['genre'])>0:
                self._genre_entry.insert(tk.END, self._current_metadata['genre'])
        except Exception as e:
            print(e)