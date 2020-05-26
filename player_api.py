from flask import Flask, request
from backend_manager import BackendManager
from song import Song
from playlist import Playlist
import json
import random

app = Flask(__name__)

backend_manager = BackendManager('backend.sqlite')

######################################################
# song routes
######################################################

@app.route('/song', methods=['POST'])
def add_song():
    """ Add a song to the database """
    content = request.json

    if 'genre' not in content.keys():
        content['genre'] = None

    try:
        song = Song(content['title'],
                    content['artist'],
                    content['album'],
                    content['runtime'],
                    content['file_path'],
                    content['genre'],
                    content['playlists']
                    )
        backend_manager.add_song(song)

        response = app.response_class(
            status=200
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response


@app.route('/update_plays', methods=['POST'])
def play_song():
    """ Updates the play count and last played values in the database """
    song_data = request.json
    song = backend_manager.get_song(song_data)
    
    try:
        backend_manager.increment_plays(song)
    except IndexError:
        print(f"Song {song.title} does not exist")

    response = app.response_class(
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/song', methods=['GET'])
def get_song():
    """ Get a song from the database """
    try:
        song = backend_manager.get_song(request.json)
        if song is None:
            raise ValueError(f"song does not exist")

        response = app.response_class(
            status=200,
            response=json.dumps(song.meta_data()),
            mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=404
        )
        return response

@app.route('/song/all', methods=['GET'])
def get_all_songs():
    """ Return a list of all song titles    """
    songs = backend_manager.get_all_songs()

    response = app.response_class(
        status=200,
        response=json.dumps([s.meta_data() for s in songs]),
        mimetype='application/json'
    )

    return response

@app.route('/song', methods=['DELETE'])
def delete_song():
    """ Delete a song from the DB   """
    try:
        backend_manager.delete_song(request.json)
        response = app.response_class(
            status=200
        )
    except IndexError:
        print(f"Song {request.json['title']} does not exist")

    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=404
        )
    return response


@app.route('/song', methods=['PUT'])
def edit_metadata():
    """ Update songs metadata in database """
    new_data = request.json['new']
    old_data = request.json['old']

    song = backend_manager.get_song(old_data)

    if 'genre' not in new_data.keys():
        new_data['genre'] = None
    try:
        if new_data['title'] is not song.title:
            song.title = new_data['title']
            print("new title:",song.title)
        if new_data['artist'] is not song.artist:
            song.artist = new_data['artist']
            print("new artist:",song.artist)
        if new_data['album'] is not song.album:
            song.album = new_data['album']
            print("new album:",song.album)
        if new_data['rating'].isnumeric():
            song.set_rating(new_data['rating'])
        if new_data['genre'] is not "":
            song.genre = new_data['genre']

        backend_manager.commit_new_metadata(song, old_data)
        response = app.response_class(
            status=200
        )
    
    except ValueError as e:
        print(e)
        response = app.response_class(
            response=str(e),
            status=400
        )

    return response

@app.route('/song/all', methods=['DELETE'])
def delete_all_songs():
    """ Delete a song from the DB   """
    try:
        backend_manager.delete_all_songs()
        response = app.response_class(status=200)
    except ValueError as e:
        response = app.response_class(response=str(e), status=404)
    return response


######################################################
# filter routes
######################################################

@app.route('/filter/multi', methods=['GET'])
def filter_library_by_multi():
    """ filters library """
    the_filter = request.json
    filter_results = backend_manager.filter_library(the_filter)
    songs = list(filter_results.values())
    response = app.response_class(
            status=200,
            response=json.dumps([s.meta_data() for s in songs]),
            mimetype='application/json'
        )
    return response


######################################################
# playlist routes
######################################################

@app.route('/playlist', methods=["POST"])
def new_playlist():
    """ save new playlist to db """
    playlist_data = request.json
    try:
        playlist = Playlist(playlist_data['playlist_name'], playlist_data['playlist_desc'])
        backend_manager.new_playlist(playlist)

        response = app.response_class(
            status=200
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response

@app.route('/playlist/<string:playlist_name>', methods=['GET'])
def get_playlist(playlist_name: str):
    """ get all songs in playlist """
    try:
        all_songs = backend_manager.get_all_songs()
        playlist_songs = {}
        count=0

        for song in all_songs:
            playlists = song.playlists.replace(":..:", " ")
            if playlists.find(playlist_name) > -1:
                playlist_songs[count] = song
                count+=1
        
        response = app.response_class(
            status=200,
            response=json.dumps([s.meta_data() for s in playlist_songs.values()]),
            mimetype='application/json'
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response

@app.route('/playlist/all', methods=['GET'])
def get_all_playlists():
    """ get a list of all playlists """
    try:
        all_playlists = backend_manager.get_all_playlists()
        count = 0
        playlists={}
        for playlist in all_playlists:
            playlists[count]=playlist.playlist_name
            count+=1
        response = app.response_class(
            status=200,
            response=json.dumps(playlists),
            mimetype='application/json'
        )
    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=400
        )
    return response


@app.route('/playlist', methods=['DELETE'])
def delete_playlist():
    """ delete playlist from db """
    try:
        backend_manager.delete_playlist(request.json['playlist_name'])
        response = app.response_class(
            status=200
        )
    except IndexError:
        print(f"Song {request.json['playlist_name']} does not exist")

    except ValueError as e:
        response = app.response_class(
            response=str(e),
            status=404
        )
    return response

@app.route('/playlist/add', methods=['PUT'])
def song_playlist_association():
    """ creates an association between a song and a playlist"""
    data_nest = request.json
    print("in api:", data_nest)
    try:
        backend_manager.associate_song_and_playlist(data_nest['playlist_name'], data_nest['song'])
        response = app.response_class(
            status=200
        )
    
    except ValueError as e:
        print(e)
        response = app.response_class(
            response=str(e),
            status=400
        )

    return response

@app.route('/playlist/delete', methods=['PUT'])
def delete_song_playlist_association():
    """ deletes an association between a song and a playlist"""
    data_nest = request.json
    print("in api:", data_nest)
    try:
        backend_manager.delete_song_and_playlist_association(data_nest['playlist_name'], data_nest['song'])
        response = app.response_class(
            status=200
        )
    
    except ValueError as e:
        print(e)
        response = app.response_class(
            response=str(e),
            status=400
        )

    return response

if __name__ == "__main__":
    app.run(debug=True)
