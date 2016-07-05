import typing

from statsbiblioteket.harvest.harvest_types import Project, DayEntry, Expense
from statsbiblioteket.harvest.rest import Rest


class Projects(Rest):
    def projects(self, client_id: str =None) -> typing.List[Project]:
        """
        Get all the projects (optinally restricted to a particular client)
        """
        params = {}
        if client_id:
            # You can filter by client_id and updated_since.
            # For example to show only the projects belonging to client with the id 23445.
            # GET /projects?client=23445
            params = {'client': client_id}
        return self._get('/projects', params=params)

    def projects_for_client(self, client_id: str) -> typing.List[Project]:
        """
        Get the projects for a particular client
        """
        params = {'client': client_id}

        url = '/projects'
        return self._get(url, params=params)

    def timesheets_for_project(self, project_id, start_date, end_date) -> \
    typing.List[DayEntry]:
        """
        Get the timesheets for a project
        """
        params = {'from': start_date,
                  'to': end_date}

        url = '/projects/{0}/entries'.format(project_id)
        return self._get(url, params=params)

    def expenses_for_project(self, project_id, start_date, end_date) -> \
    typing.List[Expense]:
        """
        Get the expenses for a project between a start date and end date
        """
        params = {'from': start_date, 'to': end_date}

        url = '/projects/{0}/expenses'.format(project_id)
        return self._get(url)

    def get_project(self, project_id) -> Project:
        """
        Get a particular project
        """
        url = '/projects/{0}'.format(project_id)
        return self._get(url)

    def create_project(self, project) -> str:
        """
        Create a project and return the project id
        """
        return self._post('/projects', data=project)

    def update_project(self, project_id, project:Project):
        """
        Update a project
        Post similar XML or JSON as with create a new project, but include
        project-id as part of the project.
        """
        url = '/projects/{0}'.format(project_id)
        return self._put(url, data=project)

    def toggle_project_active(self, project_id):
        """
        Toggle the active flag of a project
        """
        return self._put('/projects/{0}/toggle'.format(project_id))

    def delete_project(self, project_id):
        """
        Delete a project

        If the project does not have any timesheet data tracked to it, it is
        deleted with HTTP Response: 200 OK. If the project does have timesheet
        entries associated, the project is not deleted and
        HTTP Response: 400 Bad Request is returned.
        """
        url = '/projects/{0}'.format(project_id)
        return self._delete(url)

    # User Assignment: Assigning users to projects

    def assign_user_to_project(self, project_id, user_id):
        """
        ASSIGN A USER TO A PROJECT
        POST /projects/#{project_id}/user_assignments
        """
        url = '/projects/{0}/user_assignments'.format(project_id)
        data = {"user": {"id": user_id}}
        return self._post(url, data)
