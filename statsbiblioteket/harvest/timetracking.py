from statsbiblioteket.harvest.harvest_types import Day, DayEntry
from statsbiblioteket.harvest.rest import Rest

class Timetracking(Rest):
    # Time Tracking

    def today(self) -> Day:
        """ today property """
        return self._get('/daily', params={'slim': 1})

    def get_day(self, day_of_the_year=1, year=2012) -> Day:
        """
        Get time tracking for a day of a particular year
        """
        url = '/daily/{0}/{1}'.format(day_of_the_year, year)
        return self._get(url,params={'slim': 1})

    def get_day_entry(self, entry_id) -> DayEntry:
        """
        Get a time entry by entry_id
        """
        url = '/daily/show/{0}'.format(entry_id)
        return self._get(url,params={'slim': 1})

    def toggle_timer(self, entry_id):
        """
        Toggle the timer for an entry
        """
        url = '/daily/timer/{0}'.format(entry_id)
        return self._get(url,params={'slim': 1})

    def add_day_entry(self, day_entry:DayEntry):
        """
        Create a new time entry?
        """
        return self._post('/daily/add', day_entry)

    def add_day_entry_for_user(self, user_id, day_entry:DayEntry):
        """
        Add data for a user
        """
        url = '/daily/add'
        return self._post(url, data=day_entry, params={'of_user':user_id})

    def delete_day_entry(self, entry_id):
        """
        Delete an entry
        """
        url = '/daily/delete/{0}'.format(entry_id)
        return self.delete_day_entry(url)

    def update_day_entry(self, entry_id, day_entry:DayEntry):
        """
        Update an entry
        """
        url = '/daily/update/{0}'.format(entry_id)
        return self._post(url, data=day_entry)
