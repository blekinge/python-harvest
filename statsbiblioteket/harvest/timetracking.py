from statsbiblioteket.harvest.rest import Rest

class Timetracking(Rest):
    # Time Tracking

    @property
    def today(self):
        """ today property """
        return self._get('/daily')

    def get_day(self, day_of_the_year=1, year=2012):
        """
        Get time tracking for a day of a particular year
        """
        url = '/daily/{0}/{1}'.format(day_of_the_year, year)
        return self._get(url)

    def get_entry(self, entry_id):
        """
        Get a time entry by entry_id
        """
        url = '/daily/show/{0}'.format(entry_id)
        return self._get(url)

    def toggle_timer(self, entry_id):
        """
        Toggle the timer for an entry
        """
        url = '/daily/timer/{0}'.format(entry_id)
        return self._get(url)

    def add_entry(self, data):
        """
        Create a new time entry?
        """
        return self._post('/daily/add', data)

    def add_entry_for_user(self, user_id, data):
        """
        Add data for a user
        """
        url = '/daily/add'
        return self._post(url, data=data, params={'of_user':user_id})

    def delete_entry(self, entry_id):
        """
        Delete an entry
        """
        url = '/daily/delete/{0}'.format(entry_id)
        return self.delete_entry(url)

    def update_entry(self, entry_id, data):
        """
        Update an entry
        """
        url = '/daily/update/{0}'.format(entry_id)
        return self._post(url, data)
