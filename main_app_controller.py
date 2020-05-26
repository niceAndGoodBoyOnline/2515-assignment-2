import tkinter as tk
from math import floor
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os
import requests
import vlc
import eyed3
from player_window import PlayerWindow
from url_window import UrlWindow
from edit_metadata import EditMetadata
from filter_library import FilterLibrary
from new_playlist import NewPlaylistlWindow
from playlists import PlaylistsWindow


class MainAppController(tk.Frame):
    """ Main Application Window
    """

    def __init__(self, parent: tk.Tk):
        """ Create the views """
        tk.Frame.__init__(self, parent)
        self._root_win = tk.Toplevel()
        self._uri = "http://localhost:5000/"
        self._player_window = PlayerWindow(self._root_win, self)
        self.cache_library_callback()
        self._vlc_instance = vlc.Instance()
        self._player = self._vlc_instance.media_player_new()
        self._currently_playing = ""
        self._current_playlist = ""
        self._playlist_songs = []
        self.playlist_position = 0
        self.feedback = self._player_window.set_info
        self._repeat = True
        self.events = self._player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.playlist_song_ended)

    ##################################
    # Song related methods
    ##################################

    def delete_callback(self):
        """ Deletes selected song. """
        try:
            song_data = self._get_song_info()
            response = requests.delete(f"{self._uri}song", json=song_data)

            if response.status_code == 200:
                self.feedback(song_data['title'] + " Deleted")
                self.cache_library_callback()
            else:
                self.feedback( 'ERROR: song was not deleted')
        except Exception as e:
            print(e)
            self.feedback("Select a song to delete first")

    def _get_song_info(self):
        """ gets currently selected song and returns information about it """
        library = self._player_window.library
        selected_info = library.get(library.curselection())
        selected_info = selected_info.split(".")
        title = selected_info[0].replace("Title: ", "").strip()
        artist = selected_info[1].replace("Artist: ", "").strip()
        album = selected_info[2].replace("Album: ", "").strip()
        return {"title":title,"artist":artist,"album":album}
    

    def play_callback(self):
        """ Play audio file. """      
        try:
            song_data = self._get_song_info()
            response = requests.get(f"{self._uri}song", json=song_data)

            media_file = response.json()['file_path']

            media = self._vlc_instance.media_new_path(media_file)

            song_meta = song_data["title"],song_data['artist'],song_data['album']
            
            if self._player.get_state() == vlc.State.Playing and self._currently_playing == song_meta:
                self._player.pause()
                self._player_window.set_icon(True)
                self._player_window.feedback['text'] = song_data['title']+" paused"
            elif self._player.get_state() == vlc.State.Paused:
                self._player.pause()
                self._player_window.set_icon(False)
                self.feedback(song_data['title']+" playing")
            elif self._currently_playing != song_meta:
                self._currently_playing = song_meta
                self._player.set_media(media)
                self._player.play()
                self._player_window.set_icon(False)
                self.feedback(song_data['title']+" playing")
        except tk.TclError as e:
            #print(e)
            self.feedback( "Select a song to play, then hit the play button")

    def add_from_file_callback(self):
        """ Loads file from local machine. """
        self._player_window.toggle_window_depth()
        selected_file = askopenfilename(initialdir='.', filetypes=(("MP3 File", "*.mp3"),))
        self._player_window.toggle_window_depth()

        if not selected_file:
            return
        adjusted_path = selected_file.replace("/", os.sep)

        data = MainAppController.__load_file(adjusted_path)

        response = requests.post(f"{self._uri}song", json=data)

        if response.status_code == 200:
            self.feedback("Song added to library")
            self.cache_library_callback()
        else:
            self.feedback("ERROR: Song not added to library")


    def add_music_folder(self):
        """ adds a folder of music """
        # use something like files = filedialog.askopenfilename(multiple=True) and a for loop
        self.feedback('Sorry, not implemented yet!')
        pass


    def add_url_callback(self):
        """ add remote song to db, supports all media files vlc supports """
        url = self._url.get_url()['URL']
        url_chunk = url.split("/")
        url_file_name = url_chunk[len(url_chunk) - 1].split(".")

        url_response = requests.get(url)

        if not os.path.exists('music'):
            os.makedirs('music')

        file_path = os.path.join('music', 'url_audio'+url_file_name[1]).replace("/", os.sep)

        with open(file_path, "wb") as f:
            f.write(url_response.content)

        if url_file_name[1] == ".mp3" or url_file_name[1] == ".mp4":
            data = MainAppController.__load_file(file_path)
            new_file_path = os.path.join('music', f"{data['title']}{url_file_name[1]}")
        else:
            new_file_path = os.path.join('music', f"{url_file_name[0]}{url_file_name[1]}")
            data ={
                "title":url_file_name[0],
                "artist":url_chunk[3],
                "album":url_chunk[3],
                "genre":" ",
                "runtime": "unknown",
                "file_path": new_file_path,
                "playlists":""}

        if not os.path.exists(new_file_path):
            os.rename(file_path, new_file_path)
        else:
            self.feedback( f"{data['title']} already exists. Adding from local machine.")
            os.remove(file_path)
        data['file_path'] = new_file_path

        response = requests.post(f"{self._uri}song", json=data)
        if response.status_code == 200:
            self.feedback( f"{data['title']} added to the database")
            self._close_url_callback()
            self.cache_library_callback()
        else:
            self.feedback( 'Something went wrong, song not added.')

    def open_url_callback(self):
        """ show add url window """
        self._url_win = tk.Toplevel()
        self._url = UrlWindow(self._url_win, self.add_url_callback, self._close_url_callback)

    def _close_url_callback(self):
        """ cloase add url window """
        self._url_win.destroy()

    ##################################
    # Library listbox related methods
    ##################################

    def open_edit_metadata_callback(self):
        """ Show update popup window """
        try:
            song_data = self._get_song_info()
            response = requests.get(f"{self._uri}song", json=song_data)
            meta_data = response.json()
            if meta_data['rating'] != "None" and meta_data['rating'] != None:
                meta_data['rating'] = int(meta_data['rating'])
            self._edit_win = tk.Toplevel()
            self._edit = EditMetadata(self._edit_win, self.commit_metadata_callback, self._close_edit_metadata_callback, meta_data)
            self._edit.set_metadata()
        except tk.TclError as e:
            print(e)
            self.feedback("Select a song to edit it's metadata")

    def _close_edit_metadata_callback(self,event):
        """ Close update Popup """
        self._edit_win.destroy()

    def commit_metadata_callback(self, event):
        """ Update audio file's metadata in db """
        try:
            metadata_nest = self._edit.get_new_metadata()

            response = requests.put(f"{self._uri}song",json=metadata_nest)
            if response.status_code == 200:
                self.feedback(f"{metadata_nest['new']['title']}'s metadata changed")
                self._close_edit_metadata_callback(event)
                self.cache_library_callback()
            else:
                self.feedback(f"ERROR: {metadata_nest['old']['title']}'s' metadata not changed")
        except Exception as e:
            print(e)
            self.feedback(f"ERROR: {metadata_nest['old']['title']}'s' metadata not changed")

    def open_filter_library_callback(self):
        """ opens window to filter library """
        self._filter_win = tk.Toplevel()
        self._filter = FilterLibrary(self._filter_win,self.filter_callback, self.cache_library_callback,self._close_filter_library_callback)

    def _close_filter_library_callback(self):
        """ closes filter libary window """
        self._filter_win.destroy()

    def filter_callback(self):
        """ passes filter to backend """
        the_filter = self._filter.get_filter_info()
        response = requests.get(f"{self._uri}filter/multi", json=the_filter)
        self.song_list = response.json()
        song_list = [f'Title: {s["title"]}. Artist: {s["artist"]}. Album: {s["album"]}. Runtime: {s["runtime"]}.' for s in response.json()]
        self._player_window.set_library_songs(song_list)

    def cache_library_callback(self):
        """ makes a list of songs in library """
        response = requests.get(f"{self._uri}song/all")
        self.song_list = response.json()
        song_list = [f'Title: {s["title"]}. Artist: {s["artist"]}. Album: {s["album"]}. Runtime: {s["runtime"]}.' for s in response.json()]
        self._player_window.set_library_songs(song_list)

    ##################################
    # Playlist listbox related methods
    ##################################

    def cache_playlist_callback(self):
        """ get songs in playlist """
        try:
            self._playlist_songs = requests.get(f"{self._uri}playlist/{self._current_playlist}")
            song_list = [f'"{s["title"]}" by {s["artist"]}. Runtime:{s["runtime"]}' for s in self._playlist_songs.json()]
            self._playlist_songs = list(self._playlist_songs.json())
            self._player_window.set_playlist_songs(song_list)
        except Exception as e:
            print(e)

    def open_new_playlist_callback(self):
        """ show new playlist window """
        self._new_playlist_win = tk.Toplevel()
        self._new_playlist = NewPlaylistlWindow(self._new_playlist_win, self.save_playlist_callback, self._close_new_playlist_callback)

    def _close_new_playlist_callback(self):
        """ close new playlist window """
        self._new_playlist_win.destroy()
    
    def save_playlist_callback(self):
        """ save new playlist to db """
        try:
            playlist_data = self._new_playlist.get_playlist_data()
            response = requests.post(f"{self._uri}playlist", json=playlist_data)

            if response.status_code == 200:
                self.feedback(f"{playlist_data['playlist_name']} created")
                self._close_new_playlist_callback()
            else:
                self.feedback(f"{playlist_data['playlist_name']} not created")
        except Exception as e:
            print(e)
            self.feedback(f"ERROR: {playlist_data['playlist_name']}'s not created")
        
    def open_playlists_callback(self):
        """ opens list of playlists """
        self._playlists_win = tk.Toplevel()
        self._playlists = PlaylistsWindow(self._playlists_win, self.load_playlist_callback, \
            self.playlist_description_callback, self.delete_playlist_callback, \
            self._close_playlists_callback)
        response = requests.get(f"{self._uri}/playlist/all")
        playlist_list = list(response.json().values())
        self._playlists.set_playlist_songs(playlist_list)

    def _close_playlists_callback(self):
        """ closes list of playlists """
        self._playlists_win.destroy()

    def add_song_to_playlist_callback(self):
        """ Adds song to playlist. """
        song_data = self._get_song_info()
        res = requests.get(f"{self._uri}song",json=song_data)
        data_nest = {"song": res.json(), "playlist_name": self._current_playlist}
        response = requests.put(f"{self._uri}playlist/add", json=data_nest)

        if response.status_code == 200:
            self.cache_playlist_callback()

    def load_playlist_callback(self):
        """ loads all the songs associated with the selected playlist """
        self._current_playlist = self._playlists.get_playlist_info()['playlist_name']
        self._player_window.set_playlist_name(self._current_playlist)
        self.cache_playlist_callback()
        self.playlist_position = 0

    def playlist_description_callback(self):
        """ displays playlist description in messagebox... maybe? """
        pass

    def delete_playlist_callback(self):
        """ removes a playlist from the db """
        try:
            playlist_data = self._playlists.get_playlist_info()
            response = requests.delete(f"{self._uri}/playlist", json=playlist_data)

            if response.status_code == 200:
                if self._current_playlist == playlist_data['playlist_name']:
                    self._current_playlist = ""
                    self.cache_playlist_callback()
                self.feedback = "Playlist deleted"
            else:
                self.feedback = "Could not delete playlist"
        except Exception as e:
            print(e)
            self.feedback("select a playlist to delete first")

    def delete_song_from_playlist_callback(self):
        """ delete song and playlist association """
        try:
            song_data = self._get_song_info()
            res = requests.get(f"{self._uri}song",json=song_data)
            data_nest = {"song": res.json(), "playlist_name": self._current_playlist}
            response = requests.put(f"{self._uri}playlist/delete", json=data_nest)

            if response.status_code == 200:
                self.cache_playlist_callback()
        except Exception as e:
            print(e)
            self.feedback("Select a song to remove from this playlist")

    def play_playlist_callback(self):
        """ plays songs from playlist """
        try:
            if (len(self._playlist_songs) - 1) != self.playlist_position:
                media_file = self._playlist_songs[self.playlist_position]['file_path']
                media = self._vlc_instance.media_new_path(media_file)
                self._player.set_media(media)
                self._player.play()
                self.feedback( "playing: " + self._playlist_songs[self.playlist_position]['title'])
                self.playlist_position += 1
            elif self._repeat:
                self.playlist_position = 0
                self.play_playlist_callback
            else:
                self.feedback("playlist has ended")
        except Exception as e:
            print(e)
            self.feedback("Load a playlist first!")

    def play_previous_callback(self):
        """ Plays previous song in playlist. """
        if self.playlist_position >= 0:
            try:
                self.playlist_position -= 2

                media_file = self._playlist_songs[self.playlist_position]['file_path']

                media = self._vlc_instance.media_new_path(media_file)

                self._player.set_media(media)
                self._player.play()
                self.feedback( f"playing {self._playlist_songs[self.playlist_position]['title']}" )
            except IndexError:
                self.playlist_position = len(self._playlist_songs) - 1
                self.play_playlist_callback()
        else:
            self.playlist_position = len(self._playlist_songs) - 1
            self.play_playlist_callback()
            self.feedback( "You went all the way around to the end!" )

    def play_next_callback(self):
        """ Plays next song in playlist. """
        if self.playlist_position <= len(self._playlist_songs) - 1:
            try:
                
                media_file = self._playlist_songs[self.playlist_position]['file_path']
                media = self._vlc_instance.media_new_path(media_file)

                self._player.set_media(media)
                self._player.play()
                self.feedback( f"playing {self._playlist_songs[self.playlist_position]['title']}" )
                self.playlist_position += 1
            except IndexError:
                self.playlist_position = 0
                self.play_playlist_callback()
        else:
            self.playlist_position = 0
            self.play_playlist_callback()
            self.feedback( "No songs left in playlist, going back to the start!" )

    def playlist_song_ended(self,event):
        """ an event listener? idk """
        self.play_playlist_callback()

    
    ##################################
    # Misc methods
    ##################################

    def quit_callback(self):
        """ Exit the application. """
        self.master.quit()

    @classmethod
    def __load_file(cls, selected_file: str) -> dict:
        """ loads the mp3 file data using eyed3 tags. """
        audio = eyed3.load(selected_file)

        title = cls.get_tag(audio, "title")
        artist = cls.get_tag(audio, "artist")
        album = cls.get_tag(audio, "album")
        genre = cls.get_tag(audio, "genre._name")

        runtime_secs = audio.info.time_secs
        runtime_mins = int(runtime_secs // 60)

        runtime = str(runtime_mins) + ':' + str(floor(runtime_secs) - (runtime_mins * 60))

        data = {'title': title,
                'artist': artist,
                'album': album,
                'runtime': runtime,
                'file_path': selected_file,
                'genre': genre,
                'playlists': ""}
        return data

    @staticmethod
    def get_tag(file, tag: str):
        """ Static method to get eyed3 tags for mp3 files. """
        try:
            return str(getattr(file.tag, tag))
        except AttributeError:
            return "None"


if __name__ == "__main__":
    """ Create Tk window manager and a main window. Start the main loop """
    root = tk.Tk()
    MainAppController(root).pack()
    tk.mainloop()
