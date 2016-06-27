from statsbiblioteket.harvest.rest import Rest


class TaskAssignments(Rest):
    # Task Assignment: Assigning tasks to projects

    def get_all_tasks_from_project(self, project_id):
        """
        GET ALL TASKS ASSIGNED TO A GIVEN PROJECT
        /projects/#{project_id}/task_assignments
        """
        url = '/projects/{0}/task_assignments'.format(project_id)
        return self._get(url)

    def get_one_task_assigment(self, project_id, task_id):
        """
        GET ONE TASK ASSIGNMENT
        GET /projects/#{project_id}/task_assignments/#{task_assignment_id}
        """
        url = '/projects/{0}/task_assignments/{1}'.format(project_id, task_id)
        return self._get(url)

    def assign_task_to_project(self, project_id, **kwargs):
        """
        ASSIGN A TASK TO A PROJECT
        POST /projects/#{project_id}/task_assignments
        """
        url = '/projects/{0}/task_assignments/'.format(project_id)
        return self._post(url, kwargs)

    def create_task_to_project(self, project_id, **kwargs):
        """
        CREATE A NEW TASK AND ASSIGN IT TO A PROJECT
        POST /projects/#{project_id}/task_assignments/add_with_create_new_task
        """
        url = '/projects/{0}/task_assignments/add_with_create_new_task'.format(
            project_id)
        return self._post(url, kwargs)

    def remove_task_from_project(self, project_id, task_id):
        """
        REMOVING A TASK FROM A PROJECT
        DELETE /projects/#{project_id}/task_assignments/#{task_assignment_id}
        """
        url = '/projects/{0}/task_assignments/{1}'.format(project_id, task_id)
        return self._delete(url)

    def change_task_from_project(self, project_id, task_id, data, **kwargs):
        """
        CHANGING A TASK FOR A PROJECT
        PUT /projects/#{project_id}/task_assignments/#{task_assignment_id}
        """
        url = '/projects/{0}/task_assignments/{1}'.format(project_id, task_id)
        kwargs.update({'task-assignment': data})
        return self._put(url, kwargs)
