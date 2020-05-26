from sqlalchemy import Column, Text, Integer
from audio_file import AudioFile
from datetime import datetime, time
from typing import Dict
from usage_stats import UsageStats

class Song(AudioFile):
    """ Models a single song that can be played by an audio player.
    Author: Felix Ruttan    
    """

    album = Column(Text)
    genre = Column(Text)
    rating = Column(Integer)
    playlists = Column(Text)

    def __init__(self, title: str, artist: str, album: str, runtime: str, file_path: str,  genre: str = None, rating: int = None):
        """Creates an instance of a song"""

        if not isinstance(album, str):
            raise ValueError("album must be a string")
        if genre is not None and isinstance(genre, str):
            self._genre = genre
        else:
            self._genre = None

        super().__init__(title, artist, runtime, file_path)
        self.album = album
        self.playlists = ""
        if rating is not None and isinstance(rating, int):
            self.rating = rating
        else:
            self.rating = None

    def set_genre(self, update: str):
        """ setter for the genre attribute """
        try:
            if self.genre is not None and update.strip() not in self.genre:
                self.genre += ",", update
            else:
                self.genre = update
        except TypeError:
            print("genre must be string")

    def meta_data(self) -> Dict:
        """returns a dictionary of song meta data"""
        meta_dict = {
            "title": str(self.title),
            "artist": str(self.artist),
            "album": str(self.album),
            "date_added": str(self.date_added),
            "runtime": str(self.runtime),
            "file_path": str(self.file_path),
            "genre": str(self.genre),
            "play_count": str(self.play_count),
            "last_played": str(self.last_played),
            "rating": str(self.rating),
            "playlists": str(self.playlists)
        }
        return meta_dict

    def get_description(self) -> str:
        """prints out details about the song object"""
        try:
            song_details = "{} by {} from the album {} added on {}. Runtime is {}." \
                .format(self.title, self.artist, self.album, self._usage._date_added, self.runtime)

            if self._usage.last_played is not None:
                song_details += " Last played on " + str(self._usage.last_played) + "."
            if self.rating is not None:
                song_details += " User rating is " + str(self.rating) + "/5."
        except AttributeError:
            song_details = "Song is missing info, cannot display"

        return song_details

    def increment_song_plays(self):
        """ adds 1 to play value and sets last_played to now """
        self.play_count += 1
        self.last_played = datetime.now()

    def add_playlist(self, playlist: str):
        """ adds the name of a playlist to self.playlists """
        self.playlists += playlist+':..:'

    def delete_playlist(self, playlist: str):
        """ remotes playlist from self.playlists """
        self.playlists.place(playlist+":..:", "")

    def update(self, object):
        """ updates the instance variables of the song object with the object supplied """

        if isinstance(object, Song):
            self.artist = object.artist
            self.album = object.album
            self.title = object.title
            self.genre = object.genre
            self.rating = object.rating
            self.playlists = object.playlists

    def set_rating(self, update):
        """ setter for the rating of the song """
        self.rating = update
        print(self.rating)