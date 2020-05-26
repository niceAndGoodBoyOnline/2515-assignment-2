from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from base import Base
from datetime import datetime
from song import Song
from playlist import Playlist


class BackendManager:

    def __init__(self, db_filename):
        """ Initializes the list of songs """

        if db_filename is None or db_filename == "":
            raise ValueError("Invalid Database File")

        engine = create_engine('sqlite:///' + db_filename)

        # Bind the engine to the metadata fo the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self._db_session = sessionmaker(bind=engine)

    ### song methods

    def add_song(self, song: Song):
        """ Adds a new song """

        if song is None or not isinstance(song, Song):
            raise ValueError("Invalid Song Object")

        session = self._db_session()     
        session.add(song)
        session.commit()

        song_id = song.id

        session.close()

        return song_id

    def commit_new_metadata(self, object: Song, old_data: dict):
        """ commit new metadata to db """
       
        session = self._db_session()

        existing_song = session.query(Song).filter(
            Song.title == old_data['title'],
            Song.artist == old_data['artist'],
            Song.album == old_data['album']).first()
        
        if existing_song is None:
            raise ValueError(f"Song {object.title} does not exist")

        existing_song.update(object)

        session.commit()
        session.close()

    def increment_plays(self, song: Song):
        """ adds a play to songs metadata in the db """
        session = self._db_session()

        existing_song = session.query(Song).filter(
            Song.title == song.title,
            Song.artist == song.artist,
            Song.album == song.album).first()
        if existing_song is None:
            raise ValueError(f"Song {song.title} does not exist")

        existing_song.increment_plays()

        session.commit()
        session.close

    def get_song(self, data: dict) -> Song:
        """ Return song object matching title, artist and album"""

        if data is None or type(data) != dict:
            raise ValueError("Invalid Song Data")

        session = self._db_session()

        song = session.query(Song).filter(
                Song.title == data['title'],
                Song.artist == data['artist'],
                Song.album == data['album']).first()

        session.close()

        return song

    def delete_song(self, data: dict):
        """ Delete a song from the database """
        
        if data is None or type(data) != dict:
            raise ValueError("Invalid Song Data")
        print("in_backend:",data)
        session = self._db_session()

        song = session.query(Song).filter(
                Song.title == data['title'],
                Song.artist == data['artist'],
                Song.album == data['album']).first()
        session.delete(song)
        session.commit()
        session.close()


    def get_all_songs(self):
        """ Return a list of all songs in the DB """
        session = self._db_session()

        all_songs = session.query(Song).all()
        session.close()

        return all_songs

    def delete_all_songs(self):
        """ Delete all songs from the database """

        session = self._db_session()
        session.query(Song).delete()
        session.commit()
        session.close

    ################################
    ### filter methods
    ################################

    def filter_library(self, incoming_filter: dict):
        """ query server based on multiple filter parameters """
        session = self._db_session()
        songs = self.get_all_songs()
        filter_results = {}
        count = 0
        # property_list = list(incoming_filter)
        # value_list = list(incoming_filter.values())
        # print(property_list)
        # print(value_list)

        for song in songs:

            if song.genre is None:
                genre = ""
            else:
                genre = song.genre
            
            if incoming_filter['title'].lower() in song.title.lower() \
            and incoming_filter['album'].lower() in song.album.lower() \
            and incoming_filter['artist'].lower() in song.artist.lower() \
            and incoming_filter['genre'].lower() in genre.lower() \
            and str(incoming_filter['rating']).lower() in str(song.rating).lower():
                filter_results[count] = song
                count+=1           
        return filter_results

    ############################
    ### playlist methods
    ############################
    def new_playlist(self, playlist: Playlist):
        """ save a new playlist to the db """
        try:
            if self.validate_playlist(playlist):
                session = self._db_session()
                session.add(playlist)
                session.commit()
                return f"{playlist.playlist_name} added"
            else:
                return  f"{playlist.playlist_name} not a valid playlist"
        except Exception as e:
            print(e)
            pass

    def get_all_playlists(self):
        """ Return a list of all playlists in the DB """
        session = self._db_session()

        all_playlists = session.query(Playlist).all()
        print(all_playlists)
        session.close()

        return all_playlists

    def get_playlist(self, playlist: str) -> Playlist or str:
        """ get a Playlist object from the db """
        
        session = self._db_session()

        db_playlist = session.query(Playlist).filter(
                Playlist.playlist_name == playlist)

        session.close()

        if self.validate_playlist(db_playlist):
            return db_playlist
        else:
            return "No playlist named", playlist, "found."

    def delete_playlist(self, playlist: str):
        """ delete a playlist from the db """

        session = self._db_session

        try:
            playlist = session.query(Playlist).flter(
                Playlist.playlist_name == playlist).first()
            session.delete(playlist)
            session.commit()
            session.close_all
        except Exception as e:
            print(e)


    def associate_song_and_playlist(self, playlist: str, song: dict):
        """ saves an association between a song and a playlist in the db """
        print("we assing", playlist)
        session = self._db_session()
        try:
            db_song = session.query(Song).filter(
                Song.title == song['title'],
                Song.artist == song['artist'],
                Song.album == song['album']).first()
            
            playlist_list = db_song.playlists.split(":..:")
            if db_song.playlists.find(playlist) < 0:
                db_song.add_playlist(playlist)
                session.commit()
                session.close()
                return "Association created"
            else:
                return "bummer, no association possible.. because it's already associated dude!"
        except Exception as e:
            print(e)
            return "bummer, no assocition possible"

    def delete_song_and_playlist_association(self, playlist: str, song: dict):
        """ deletes association between a song and a playlist in the db """
        print("we assing", playlist)
        session = self._db_session()
        try:
            db_song = session.query(Song).filter(
                Song.title == song['title'],
                Song.artist == song['artist'],
                Song.album == song['album']).first()
            
            playlist_list = db_song.playlists.split(":..:")
            if db_song.playlists.find(playlist) > -1:
                db_song.delete_playlist(playlist)
                session.commit()
                session.close()
                return "Association deleted"
            else:
                return "not associated"
        except Exception as e:
            print(e)
            return "bummer, something's up, idk what"

    def validate_song(self, song:Song) -> bool:
        """ check if song is of class Song"""
        if song is None or not isinstance(song, Song):
            return False
        else:
            return True


    def validate_playlist(self, playlist:Playlist) -> bool:
        """ checks if playlist is of class Playlist """
        if playlist is None or not isinstance(playlist, Playlist):
            return False
        else:
            return True