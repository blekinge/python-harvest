import typing

from statsbiblioteket.harvest.harvest_types import Task
from statsbiblioteket.harvest.rest import Rest


class Tasks(Rest):
    # Tasks

    def tasks(self, updated_since=None) -> typing.List[Task]:
        """
        Get all teh tasks (optionally updated since a particular date)
        /tasks?updated_since=2010-09-25+18%3A30
        """
        url = '/tasks'
        params = {}
        if updated_since is not None:
            params['updated_since'] = updated_since
        return self._get(url,params=params)

    def get_task(self, task_id) -> Task:
        """
        Get a particular task by task_id
        """
        url = '/tasks/{0}'.format(task_id)
        return self._get(url)

    def create_task(self, **kwargs):
        """
        CREATE NEW TASK
        Example: client.create_task(task={"name":"jo"})
        """
        return self._post('/tasks/', data=kwargs)

    def update_task(self, tasks_id, **kwargs):
        """
        UPDATE AN EXISTING TASK
        Example: client.update_task(task_id, task={"name": "jo"})
        """
        url = '/tasks/{0}'.format(tasks_id)
        return self._put(url, data=kwargs)

    def delete_task(self, tasks_id):
        """
        ARCHIVE OR DELETE EXISTING TASK
        Returned if task does not have any hours associated - task will be deleted.
        Returned if task is not removable - task will be archived.
        """
        url = '/tasks/{0}'.format(tasks_id)
        return self._delete(url)

    def activate_task(self, tasks_id):
        """
        ACTIVATE EXISTING ARCHIVED TASK
        """
        url = '/tasks/{0}/activate'.format(tasks_id)
        return self._post(url)
