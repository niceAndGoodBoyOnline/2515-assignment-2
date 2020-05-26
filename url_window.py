import tkinter as tk


class UrlWindow(tk.Frame):
    """ Window for adding song with a url """

    def __init__(self, parent, add_callback, close_callback):
        """ Initialize the add url window """
        tk.Frame.__init__(self, parent)
        self._add = add_callback
        self._close = close_callback

        parent.title('Add URL')
        parent.lift()

        # Frames
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, padx=30, pady=0)

        self.bot_frame = tk.Frame(self.master)
        self.bot_frame.grid(row=1, padx=30, pady=0)

        # Labels and entries
        self._URL_label = tk.Label(self.top_frame, text='URL:')
        self._URL_label.grid(row=0, column=0, sticky=tk.W)

        self._URL_entry = tk.Entry(self.top_frame, width=20)
        self._URL_entry.grid(row=0, column=1, sticky=tk.E)

        # Buttons
        self.save_button = tk.Button(self.bot_frame, text='Save', width=10, command=self._add)
        self.save_button.grid(row=1)

        self.cancel_button = tk.Button(self.bot_frame, text='Close', width=10, command=self._close)
        self.cancel_button.grid(row=1, column=1)

    def get_url(self) -> dict:
        """ return url as json """
        return {'URL': self._URL_entry.get()}
