import tkinter as tk
from typing import Dict


class FilterLibrary(tk.Frame):
    """ layout for filter library window """

    def __init__(self, parent, filter_callback, unfilter_callback, close_callback):
        """ Initialize the library filter """
        tk.Frame.__init__(self, parent)
        self._filter = filter_callback
        self._revert = unfilter_callback
        self._close = close_callback
        parent.title('Filter Library')


        # Frames
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=0)

        self.bot_frame = tk.Frame(self.master)
        self.bot_frame.grid(row=1, padx=30, pady=0)

        # options object
        options = dict(
            master=self.top_frame,onvalue=True, offvalue=False
        )

        #title UI elements
        self._title_label = tk.Label(self.top_frame, text='Title:')
        self._title_label.grid(row=0, column=0, sticky=tk.N)

        self._title_entry = tk.Entry(self.top_frame, width=40)
        self._title_entry.grid(row=0, column=1, sticky=tk.N)

        #artist UI elements
        self._artist_label = tk.Label(self.top_frame, text='Artist:')
        self._artist_label.grid(row=1, column=0, sticky=tk.N)

        self._artist_entry = tk.Entry(self.top_frame, width=40)
        self._artist_entry.grid(row=1, column=1, sticky=tk.N)

        #album UI elements
        self._album_label = tk.Label(self.top_frame, text='Album:')
        self._album_label.grid(row=2, column=0, sticky=tk.N)

        self._album_entry = tk.Entry(self.top_frame, width=40)
        self._album_entry.grid(row=2, column=1, sticky=tk.N)
        
        #genre UI elements
        self._genre_label = tk.Label(self.top_frame, text='Genre:')
        self._genre_label.grid(row=3, column=0, sticky=tk.N)

        self._genre_entry = tk.Entry(self.top_frame, width=40)
        self._genre_entry.grid(row=3, column=1, sticky=tk.N)

        #rating UI elements
        self._rating_label = tk.Label(self.top_frame, text='Rating:')
        self._rating_label.grid(row=4, column=0, sticky=tk.N)

        self._rating_entry = tk.Entry(self.top_frame, width=40)
        self._rating_entry.grid(row=4, column=1, sticky=tk.N)

        # Buttons
        self.save_button = tk.Button(self.bot_frame, text='Filter Library', width=10, command=self._filter)
        self.save_button.grid(row=0)

        self.save_button = tk.Button(self.bot_frame, text='Remove Filter', width=10, command=self._revert)
        self.save_button.grid(row=0, column=1)

        self.cancel_button = tk.Button(self.bot_frame, text='Cancel', width=10, command=self._close)
        self.cancel_button.grid(row=0, column=2)

    def get_filter_info(self):
        """ grabs info from entry and returns dictionary/JSON """
        this_filter = {}
        this_filter['title'] = self._title_entry.get()
        this_filter['artist'] = self._artist_entry.get()
        this_filter['album'] = self._album_entry.get()
        this_filter['genre'] = self._genre_entry.get()
        this_filter['rating'] = self._rating_entry.get()
        return this_filter