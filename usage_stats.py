from datetime import datetime


class UsageStats:
    """ a container for usage information and statistics """

    _DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, date_added: datetime):
        """ create a usagestats object and set the date added"""
        if UsageStats.__valid_datetime(date_added):
            self._date_added = date_added
        else:
            raise ValueError("date_added must be a datetime object")

        self._play_count = 0
        self._last_played = None

    @property
    def date_added(self):
        """ return the date the song or playlist was added to the library """
        return self._date_added.strftime(UsageStats._DATE_FORMAT)

    @property
    def last_played(self):
        """ return the date the song or playlist was last played """
        if self._last_played is None:
            return None
        else:
            return self._last_played.strftime(UsageStats._DATE_FORMAT)

    @property
    def play_count(self):
        """ return the number of times the song or playlist has been played """
        return self._play_count

    def increment_usage_stats(self):
        """ update the play count and last played time when a song is played """
        self._play_count += 1
        self._last_played = datetime.now()

    @classmethod
    def __valid_datetime(cls, date):
        """ private method to validate the date is datetime object """
        if type(date) is not datetime:
            return False
        else:
            return True
