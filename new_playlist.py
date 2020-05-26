import tkinter as tk


class NewPlaylistlWindow(tk.Frame):
    """ Window for making a new playlist """

    def __init__(self, parent, save_callback, close_callback):
        """ Initialize the new playlist window """
        tk.Frame.__init__(self, parent)
        self._save = save_callback
        self._close = close_callback

        parent.title('New Playlist')
        parent.lift()

        # Frames
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=0)

        self.bot_frame = tk.Frame(self.master)
        self.bot_frame.grid(row=1, padx=30, pady=0)

        # playlist name UI
        self._playlist_name_label = tk.Label(self.top_frame, text='Playlist Name:')
        self._playlist_name_label.grid(row=0, column=0)

        self._playlist_name_entry = tk.Entry(self.top_frame, width=20)
        self._playlist_name_entry.grid(row=0, column=1)

        # playlist description UI
        self._playlist_description_label = tk.Label(self.top_frame, text='Playlist Description:')
        self._playlist_description_label.grid(row=1, column=0)

        self._playlist_description_entry = tk.Entry(self.top_frame, width=20)
        self._playlist_description_entry.grid(row=1, column=1)

        # Buttons
        self.save_button = tk.Button(self.bot_frame, text='Save Playlist', width=10, command=self._save)
        self.save_button.grid(row=10, padx=10, pady=5)

        self.cancel_button = tk.Button(self.bot_frame, text='Cancel', width=10, command=self._close)
        self.cancel_button.grid(row=11, padx=10, pady=5)

    def get_playlist_data(self) -> dict:
        """ return playlist name and description as json """
        return {'playlist_name': self._playlist_name_entry.get(),
                'playlist_desc': self._playlist_description_entry.get()
                }
