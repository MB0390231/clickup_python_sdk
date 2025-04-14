from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Task(AbstractObject):
    """
    Represents a ClickUp Task object.

    This class provides methods to interact with ClickUp tasks, including viewing, updating,
    and deleting tasks, as well as managing task-related operations such as tags, custom fields,
    file attachments, time tracking, checklists, comments, and dependencies.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Task object.

        Args:
            id (str, optional): The unique identifier of the task. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this task.

        Returns:
            str: The API endpoint path for this task.

        Raises:
            AssertionError: If the task ID is not set.
        """
        assert self["id"] != None, "Must provide task id"
        return "task" + "/" + self["id"]

    def get(
        self,
        team_id=None,
        include_subtasks=False,
        include_markdown_description=False,
        custom_fields=None,
    ):
        """
        Retrieve complete information about a task.

        Fetches task details from the ClickUp API. You can only access tasks that you have
        permission to view. Tasks with attachments will include an "attachments" field in the
        response, but document attachments are not returned.

        Args:
            team_id (str, optional): The Workspace ID. Required when custom_task_ids is enabled
                in the workspace.
            include_subtasks (bool, optional): Whether to include subtasks in the response.
                Defaults to False.
            include_markdown_description (bool, optional): Whether to return task descriptions
                in Markdown format. Defaults to False.
            custom_fields (list, optional): Filter tasks by specific Custom Field values.
                Should be a list of custom field objects.

        Returns:
            Task: The current task instance with updated task information.
        """
        route = self.get_endpoint() + "/?"
        params = {}

        if team_id is not None:
            params["team_id"] = str(team_id)

        if include_subtasks:
            params["include_subtasks"] = "true"

        if include_markdown_description:
            params["include_markdown_description"] = "true"

        if custom_fields is not None:
            if isinstance(custom_fields, list):
                import json

                params["custom_fields"] = json.dumps(custom_fields)

        if params:
            param_str = "&".join([f"{key}={value}" for key, value in params.items()])
            route += param_str

        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self

    def add_tag(self, tag_name):
        """
        Add a tag to the task.

        Args:
            tag_name (str): The name of the tag to add.

        Returns:
            Task: The current task instance with updated information.

        Example:
            task.add_tag("priority")
        """
        route = self.get_endpoint() + "/tag/" + tag_name + "/"
        method = "POST"
        response = self.api.make_request(method=method, route=route)
        return self.get()  # Refresh task data

    def remove_tag(self, tag_name):
        """
        Remove a tag from the task.

        Args:
            tag_name (str): The name of the tag to remove.

        Returns:
            Task: The current task instance with updated information.

        Example:
            task.remove_tag("priority")
        """
        route = self.get_endpoint() + "/tag/" + tag_name
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return self.get()  # Refresh task data

    def update(
        self,
        name=None,
        description=None,
        markdown_content=None,
        status=None,
        priority=None,
        due_date=None,
        due_date_time=None,
        parent=None,
        time_estimate=None,
        start_date=None,
        start_date_time=None,
        points=None,
        assignees_add=None,
        assignees_remove=None,
        group_assignees_add=None,
        group_assignees_remove=None,
        watchers_add=None,
        watchers_remove=None,
        archived=None,
        custom_item_id=None,
        custom_task_ids=None,
        team_id=None,
    ):
        """
        Update task properties with specified named parameters.

        Provides a user-friendly interface to update task details by specifying individual
        parameters instead of constructing a values dictionary manually.

        Args:
            name (str, optional): The updated name of the task.
            description (str, optional): The updated description of the task.
                To clear the description, use a single space " ".
            markdown_content (str, optional): Markdown formatted description for the task.
                If both markdown_content and description are provided, markdown_content
                will take precedence.
            status (str, optional): The new status of the task.
            priority (int, optional): The updated priority level (1-4, with 1 being highest).
            due_date (int, optional): The due date as a Unix timestamp in milliseconds.
            due_date_time (bool, optional): Whether the due date includes a time component.
            parent (str, optional): Move a subtask to another parent task by providing a valid task ID.
                Note: You cannot convert a subtask to a task by setting parent to None.
            time_estimate (int, optional): The estimated time to complete the task, in milliseconds.
            start_date (int, optional): The start date as a Unix timestamp in milliseconds.
            start_date_time (bool, optional): Whether the start date includes a time component.
            points (float, optional): The updated Sprint Points value for the task.
            assignees_add (list, optional): List of user IDs to add as assignees.
            assignees_remove (list, optional): List of user IDs to remove from assignees.
            group_assignees_add (list, optional): List of group IDs to add as assignees.
            group_assignees_remove (list, optional): List of group IDs to remove from assignees.
            watchers_add (list, optional): List of user IDs to add as watchers.
            watchers_remove (list, optional): List of user IDs to remove from watchers.
            archived (bool, optional): Whether the task should be archived.
            custom_item_id (int or None, optional): The custom task type ID.
                A value of None sets the task type to "Task".
            custom_task_ids (bool, optional): Set to True if referencing a task by its custom task ID.
            team_id (int, optional): Required when custom_task_ids is True. The Workspace ID.

        Returns:
            Task: The current task instance with updated information.

        Note:
            To update Custom Fields on a task, you must use the update_custom_field() method instead.

        Example:
            task.update(
                name="Updated Task Name",
                status="in progress",
                priority=2,
                assignees_add=[123456, 789012],
                assignees_remove=[345678]
            )
        """
        route = "task/" + self["id"] + "/"
        params = {}
        values = {}

        # Add query parameters
        if custom_task_ids:
            params["custom_task_ids"] = "true"

        if team_id is not None:
            params["team_id"] = str(team_id)

        if params:
            route += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        # Add body parameters
        if name is not None:
            values["name"] = name

        if description is not None:
            values["description"] = description

        if markdown_content is not None:
            values["markdown_content"] = markdown_content

        if status is not None:
            values["status"] = status

        if priority is not None:
            values["priority"] = priority

        if due_date is not None:
            values["due_date"] = due_date

        if due_date_time is not None:
            values["due_date_time"] = due_date_time

        if parent is not None:
            values["parent"] = parent

        if time_estimate is not None:
            values["time_estimate"] = time_estimate

        if start_date is not None:
            values["start_date"] = start_date

        if start_date_time is not None:
            values["start_date_time"] = start_date_time

        if points is not None:
            values["points"] = points

        # Handle assignees (users)
        if assignees_add is not None or assignees_remove is not None:
            assignees = {}
            if assignees_add is not None:
                assignees["add"] = assignees_add
            if assignees_remove is not None:
                assignees["rem"] = assignees_remove
            if assignees:
                values["assignees"] = assignees

        # Handle group assignees
        if group_assignees_add is not None or group_assignees_remove is not None:
            group_assignees = {}
            if group_assignees_add is not None:
                group_assignees["add"] = group_assignees_add
            if group_assignees_remove is not None:
                group_assignees["rem"] = group_assignees_remove
            if group_assignees:
                values["group_assignees"] = group_assignees

        # Handle watchers
        if watchers_add is not None or watchers_remove is not None:
            watchers = {}
            if watchers_add is not None:
                watchers["add"] = watchers_add
            if watchers_remove is not None:
                watchers["rem"] = watchers_remove
            if watchers:
                values["watchers"] = watchers

        if archived is not None:
            values["archived"] = archived

        if custom_item_id is not None:
            values["custom_item_id"] = custom_item_id

        method = "PUT"
        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def update_custom_field(self, custom_field_id=None, value=None):
        """
        Update a custom field value for the task.

        Args:
            custom_field_id (str): The ID of the custom field to update.
            value: The new value for the custom field. The format depends on the custom field type.
                Refer to the ClickUp API documentation for specific value formats for different
                custom field types.

        Returns:
            Task: The current task instance with updated information.

        Example:
            task.update_custom_field("a1b2c3", "New Value")
        """
        route = "task/" + self["id"] + "/field/" + custom_field_id
        method = "POST"
        values = {"value": value}
        response = self.api.make_request(method=method, route=route, values=values)
        # The response likely doesn't contain full task data, so fetch the task to get updated data
        return self.get()

    def delete(self):
        """
        Delete the task.

        Permanently removes the task from ClickUp.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = "task/" + self["id"] + "/"
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def upload_file(self, file):
        """
        Upload a file attachment to the task.

        Args:
            file (dict): A dictionary containing file information as required by the
                ClickUp API. This should follow the format specified in the ClickUp
                API documentation for file uploads.

        Returns:
            Task: The current task instance with updated information.

        Note:
            This method uses the requests library for file uploads.
        """
        import requests

        route = "task/" + self["id"] + "/attachment"
        method = "POST"
        response = self.api.make_request(method=method, route=route, file=file)
        return self.get()  # Refresh task data

    def get_time_in_status(self):
        """
        Get time spent in each status for the task.

        Returns information about how long the task has been in each status.

        Returns:
            dict: A dictionary containing time spent in each status. The format
                follows the ClickUp API response structure for time in status.
        """
        route = "task/" + self["id"] + "/time_in_status"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        return response  # Keep this as dictionary since it's specialized data that doesn't map to an object

    def get_subtasks(
        self, page=0, order_by=None, reverse=None, statuses=None, include_closed=None
    ):
        """
        Get all subtasks for this task.

        Retrieves subtasks that are direct children of this task.

        Args:
            page (int, optional): Page number for pagination. Defaults to 0.
            order_by (str, optional): Field to order results by (e.g., "created", "updated", "due_date").
            reverse (bool, optional): Whether to reverse the order of results.
            statuses (list, optional): List of status names to filter by.
            include_closed (bool, optional): Whether to include closed subtasks.

        Returns:
            list: A list of Task objects representing the subtasks.
        """
        route = self.get_endpoint() + "/subtask?"
        method = "GET"
        params = {"page": str(page)}

        if order_by is not None:
            params["order_by"] = order_by

        if reverse is not None:
            params["reverse"] = str(reverse).lower()

        if statuses is not None:
            if isinstance(statuses, list):
                params["statuses"] = ",".join(statuses)

        if include_closed is not None:
            params["include_closed"] = str(include_closed).lower()

        param_str = "&".join([f"{key}={value}" for key, value in params.items()])
        route += param_str

        response = self.api.make_request(method=method, route=route)

        result = []
        for subtask in response.get("tasks", []):
            task_obj = Task()
            task_obj._set_data(subtask)
            result.append(task_obj)

        return result

    def create_subtask(
        self,
        name,
        description=None,
        markdown_description=None,
        assignees=None,
        tags=None,
        status=None,
        priority=None,
        due_date=None,
        due_date_time=None,
        time_estimate=None,
        start_date=None,
        start_date_time=None,
        notify_all=None,
        links_to=None,
        check_required_custom_fields=None,
        custom_fields=None,
    ):
        """
        Create a new subtask under this task.

        Args:
            name (str): Name of the subtask (required).
            description (str, optional): Description of the subtask.
            markdown_description (str, optional): Description of the subtask in markdown format.
                If both description and markdown_description are provided, markdown_description
                will be used.
            assignees (list, optional): Array of user IDs to assign to the subtask.
            tags (list, optional): Array of tag names to apply to the subtask.
            status (str, optional): Status of the subtask. Must be a valid status name.
            priority (int, optional): Priority of the subtask (1-4, with 1 being highest).
            due_date (int, optional): Due date as a Unix timestamp in milliseconds.
            due_date_time (bool, optional): Whether the due date includes a time component.
            time_estimate (int, optional): Time estimate in milliseconds.
            start_date (int, optional): Start date as a Unix timestamp in milliseconds.
            start_date_time (bool, optional): Whether the start date includes a time component.
            notify_all (bool, optional): Whether to notify all assignees of the subtask creation.
            links_to (str, optional): Task ID to link this subtask to.
            check_required_custom_fields (bool, optional): Whether to validate that all required
                custom fields are provided.
            custom_fields (list, optional): Array of custom field objects with format:
                [{"id": "custom_field_id", "value": field_value}]

        Returns:
            Task: The created subtask as a Task object.
        """
        route = self.get_endpoint() + "/subtask"
        method = "POST"
        values = {
            "name": name,
            "parent": self["id"],
        }  # Set parent as the current task ID

        if description is not None:
            values["description"] = description
        if markdown_description is not None:
            values["markdown_description"] = markdown_description
        if assignees is not None:
            values["assignees"] = assignees
        if tags is not None:
            values["tags"] = tags
        if status is not None:
            values["status"] = status
        if priority is not None:
            values["priority"] = priority
        if due_date is not None:
            values["due_date"] = due_date
        if due_date_time is not None:
            values["due_date_time"] = due_date_time
        if time_estimate is not None:
            values["time_estimate"] = time_estimate
        if start_date is not None:
            values["start_date"] = start_date
        if start_date_time is not None:
            values["start_date_time"] = start_date_time
        if notify_all is not None:
            values["notify_all"] = notify_all
        if links_to is not None:
            values["links_to"] = links_to
        if check_required_custom_fields is not None:
            values["check_required_custom_fields"] = check_required_custom_fields
        if custom_fields is not None:
            values["custom_fields"] = custom_fields

        response = self.api.make_request(method=method, route=route, values=values)

        subtask = Task()
        subtask._set_data(response)
        return subtask

    def get_comments(self, start=None, comment_id=None):
        """
        Get all comments on this task.

        Args:
            start (int, optional): Start position for pagination.
            comment_id (str, optional): Get a specific comment by ID.

        Returns:
            list: A list of Comment objects.
        """
        from clickup_python_sdk.clickupobjects.comment import Comment

        route = self.get_endpoint() + "/comment?"
        params = {}

        if start is not None:
            params["start"] = str(start)

        if comment_id is not None:
            params["comment_id"] = comment_id

        if params:
            param_str = "&".join([f"{key}={value}" for key, value in params.items()])
            route += param_str

        method = "GET"
        response = self.api.make_request(method=method, route=route)

        result = []
        for comment_data in response.get("comments", []):
            comment = Comment.create_object(data=comment_data, target_class=Comment)
            result.append(comment)

        return result

    def create_comment(self, comment_text=None, assignee=None, notify_all=None):
        """
        Create a new comment on this task.

        Args:
            comment_text (str): The text content of the comment (required).
            assignee (int, optional): User ID to assign the comment to.
            notify_all (bool, optional): Whether to notify all watchers.

        Returns:
            Comment: The created Comment object.
        """
        from clickup_python_sdk.clickupobjects.comment import Comment

        route = self.get_endpoint() + "/comment"
        method = "POST"
        values = {"comment_text": comment_text}

        if assignee is not None:
            values["assignee"] = assignee

        if notify_all is not None:
            values["notify_all"] = notify_all

        response = self.api.make_request(method=method, route=route, values=values)
        return Comment.create_object(data=response, target_class=Comment)

    def get_checklists(self):
        """
        Get all checklists on this task.

        Returns:
            list: A list of Checklist objects.
        """
        from clickup_python_sdk.clickupobjects.checklist import Checklist

        route = self.get_endpoint() + "/checklist"
        method = "GET"
        response = self.api.make_request(method=method, route=route)

        result = []
        for checklist_data in response.get("checklists", []):
            checklist = Checklist.create_object(
                data=checklist_data, target_class=Checklist
            )
            result.append(checklist)

        return result

    def create_checklist(self, name):
        """
        Create a new checklist on this task.

        Args:
            name (str): The name of the checklist.

        Returns:
            Checklist: The created Checklist object.
        """
        from clickup_python_sdk.clickupobjects.checklist import Checklist

        route = self.get_endpoint() + "/checklist"
        method = "POST"
        values = {"name": name}

        response = self.api.make_request(method=method, route=route, values=values)
        return Checklist.create_object(data=response, target_class=Checklist)

    def add_dependency(self, depends_on_id, dependency_type=0):
        """
        Add a dependency relationship to this task.

        Args:
            depends_on_id (str): The ID of the task that this task depends on.
            dependency_type (int, optional): Type of dependency. 0 = This task waits on depends_on,
                1 = This task blocks depends_on. Defaults to 0.

        Returns:
            Dependency: The created Dependency object.
        """
        from clickup_python_sdk.clickupobjects.dependency import Dependency
        
        route = self.get_endpoint() + "/dependency"
        method = "POST"
        values = {"depends_on": depends_on_id, "type": dependency_type}

        response = self.api.make_request(method=method, route=route, values=values)
        
        dependency = Dependency()
        dependency._set_data(response)
        return dependency

    def delete_dependency(self, dependency_id):
        """
        Delete a dependency relationship from this task.

        Args:
            dependency_id (str): The ID of the dependency to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint() + f"/dependency/{dependency_id}"
        method = "DELETE"

        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def get_dependencies(self):
        """
        Get all dependencies for this task.

        Returns:
            list: A list of Dependency objects linked to this task.
        """
        from clickup_python_sdk.clickupobjects.dependency import Dependency
        
        route = self.get_endpoint() + "/dependency"
        method = "GET"

        response = self.api.make_request(method=method, route=route)
        
        result = []
        # Depends on dependencies (tasks this task depends on)
        if "depends_on" in response:
            for dep in response["depends_on"]:
                dependency = Dependency.create_object(data=dep, target_class=Dependency)
                result.append(dependency)
                
        # Dependency of dependencies (tasks that depend on this task)
        if "dependency_of" in response:
            for dep in response["dependency_of"]:
                dependency = Dependency.create_object(data=dep, target_class=Dependency)
                result.append(dependency)
                
        return result

    def track_time(
        self,
        time=None,
        description=None,
        start=None,
        end=None,
        billable=None,
        tags=None,
    ):
        """
        Track time for this task.

        Args:
            time (int, optional): Time in milliseconds. Required if start and end are not provided.
            description (str, optional): Description of the time entry.
            start (int, optional): Start time as a Unix timestamp in milliseconds.
                Required if time is not provided.
            end (int, optional): End time as a Unix timestamp in milliseconds.
                Required if time is not provided.
            billable (bool, optional): Whether the time entry is billable.
            tags (list, optional): List of tag names to apply to the time entry.

        Returns:
            TimeEntry: The created TimeEntry object.
        """
        from clickup_python_sdk.clickupobjects.timeentry import TimeEntry
        
        route = self.get_endpoint() + "/time"
        method = "POST"
        values = {}

        if time is not None:
            values["time"] = time

        if description is not None:
            values["description"] = description

        if start is not None:
            values["start"] = start

        if end is not None:
            values["end"] = end

        if billable is not None:
            values["billable"] = billable

        if tags is not None:
            values["tags"] = tags

        response = self.api.make_request(method=method, route=route, values=values)
        
        time_entry = TimeEntry()
        time_entry._set_data(response)
        return time_entry

    def get_time_entries(self, start_date=None, end_date=None, assignee=None):
        """
        Get time entries for this task.

        Args:
            start_date (int, optional): Start date as a Unix timestamp in milliseconds.
            end_date (int, optional): End date as a Unix timestamp in milliseconds.
            assignee (int, optional): Filter time entries by assignee user ID.

        Returns:
            list: A list of TimeEntry objects.
        """
        from clickup_python_sdk.clickupobjects.timeentry import TimeEntry
        
        route = self.get_endpoint() + "/time?"
        params = {}

        if start_date is not None:
            params["start_date"] = str(start_date)

        if end_date is not None:
            params["end_date"] = str(end_date)

        if assignee is not None:
            params["assignee"] = str(assignee)

        if params:
            param_str = "&".join([f"{key}={value}" for key, value in params.items()])
            route += param_str

        method = "GET"
        response = self.api.make_request(method=method, route=route)
        
        result = []
        for time_entry_data in response.get("data", []):
            time_entry = TimeEntry.create_object(data=time_entry_data, target_class=TimeEntry)
            result.append(time_entry)
            
        return result

    def start_timer(self, description=None, tags=None, billable=None):
        """
        Start a timer for this task.

        Args:
            description (str, optional): Description of the time entry.
            tags (list, optional): List of tag names to apply to the time entry.
            billable (bool, optional): Whether the time entry is billable.

        Returns:
            TimeEntry: The created TimeEntry object for the started timer.
        """
        from clickup_python_sdk.clickupobjects.timeentry import TimeEntry
        
        route = self.get_endpoint() + "/time/start"
        method = "POST"
        values = {}

        if description is not None:
            values["description"] = description

        if tags is not None:
            values["tags"] = tags

        if billable is not None:
            values["billable"] = billable

        response = self.api.make_request(method=method, route=route, values=values)
        
        time_entry = TimeEntry()
        time_entry._set_data(response)
        return time_entry

    def stop_timer(self, description=None, tags=None, billable=None):
        """
        Stop the currently running timer for this task.

        Args:
            description (str, optional): Description to add to the time entry.
            tags (list, optional): List of tag names to apply to the time entry.
            billable (bool, optional): Whether the time entry is billable.

        Returns:
            TimeEntry: The TimeEntry object for the stopped timer.
        """
        from clickup_python_sdk.clickupobjects.timeentry import TimeEntry
        
        route = self.get_endpoint() + "/time/stop"
        method = "POST"
        values = {}

        if description is not None:
            values["description"] = description

        if tags is not None:
            values["tags"] = tags

        if billable is not None:
            values["billable"] = billable

        response = self.api.make_request(method=method, route=route, values=values)
        
        time_entry = TimeEntry()
        time_entry._set_data(response)
        return time_entry
