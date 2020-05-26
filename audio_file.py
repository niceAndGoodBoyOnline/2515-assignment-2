from sqlalchemy import Column, Text, Integer, Time
from datetime import datetime, time
from os import path
from typing import Dict
from usage_stats import UsageStats
from abc import abstractmethod
from base import Base


class AudioFile(Base):
    """Models an abstract playable audio file."""

    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    artist = Column(Text, nullable=False)
    file_path = Column(Text, nullable=False)
    date_added = Column(Text, nullable=False)
    play_count = Column(Integer, nullable=False)
    last_played = Column(Text)
    runtime = Column(Time, nullable=False)

    def __init__(self, title: str, artist: str, runtime: str, file_path: str):
        """Create a new audio instance"""
        if type(self) == AudioFile:
            raise NameError("cannot create an AudioFile object")

        if not isinstance(title, str):
            raise ValueError("title of the song must be a string")
        if not isinstance(artist, str):
            raise ValueError("the artist must be a string")
        if not self.set_runtime(runtime):
            raise ValueError("the runtime must be in the format hh:mm:ss")
        if not isinstance(file_path, str):
            raise ValueError("the file path must be a string")
        if not path.exists(file_path):
            raise ValueError("file doesn't exist or is unavailable")
        self.title = title
        self.artist = artist
        self.file_path = file_path
        self._usage = UsageStats(datetime.now())
        self.last_played = self._usage.last_played
        self.play_count = self._usage.play_count
        self.date_added = self._usage.date_added

    def update_usage_stats(self):
        """plays the audio file"""
        self._usage.increment_usage_stats()

    @abstractmethod
    def get_description(self) -> str:
        """returns a description of the audio file"""
        pass

    def get_location(self) -> str:
        """ returns location of audio file """
        return self.file_path

    def get_usage_stats(self) -> UsageStats:
        """returns stats about audio file"""
        return self._usage

    @abstractmethod
    def meta_data(self) -> Dict:
       pass

    def get_play_count(self):
        return self._usage.play_count

    def set_runtime(self, runtime: str) -> bool:
        """sets runtime if valid and returns True, if not returns False"""
        time_formats = ['%S', '%M:%S','%H:%M:%S']
        try:
            self.runtime = datetime.strptime(runtime, time_formats[runtime.count(":")]).time()
            return True
        except ValueError:
            return False
