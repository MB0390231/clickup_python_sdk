from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class List(AbstractObject):
    """
    Represents a ClickUp List object.

    This class provides methods to interact with ClickUp lists, including viewing, updating,
    and creating lists, as well as managing list-related operations such as tasks, custom fields,
    and users.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a List object.

        Args:
            id (str, optional): The unique identifier of the list. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this list.

        Returns:
            str: The API endpoint path for this list.

        Raises:
            ValueError: If the list ID is not set.
        """
        if "id" not in self:
            raise ValueError("List ID is not set.")
        return "list/" + self["id"]

    def get(self):
        """
        Retrieve information about this list.

        Fetches list details from the ClickUp API. You can only access lists that
        you have permission to view.

        Returns:
            List: The current list instance with updated list information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self

    def update(
        self,
        name=None,
        content=None,
        due_date=None,
        due_date_time=None,
        priority=None,
        assignee=None,
        status=None,
    ):
        """
        Update list properties.

        Args:
            name (str, optional): The updated name of the list.
            content (str, optional): The updated content/description of the list.
            due_date (int, optional): The due date as a Unix timestamp in milliseconds.
            due_date_time (bool, optional): Whether the due date includes a time component.
            priority (int, optional): The updated priority level (1-4, with 1 being highest).
            assignee (str, optional): The ID of the user to assign to the list.
            status (str, optional): The updated status of the list.

        Returns:
            List: The current list instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {}

        if name is not None:
            values["name"] = name
        if content is not None:
            values["content"] = content
        if due_date is not None:
            values["due_date"] = due_date
        if due_date_time is not None:
            values["due_date_time"] = due_date_time
        if priority is not None:
            values["priority"] = priority
        if assignee is not None:
            values["assignee"] = assignee
        if status is not None:
            values["status"] = status

        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the list.

        Permanently removes the list from ClickUp.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def get_tasks(self, params=None):
        """
        Get tasks from this list.

        Retrieves tasks from the list with optional filtering parameters.
        Responses are limited to 100 tasks per page. This method automatically
        handles pagination to return all tasks.

        This endpoint only includes tasks where this list_id is their home List.
        Tasks added to the list with a different home List are not included in the response.

        Args:
            params (dict, optional): Dictionary of filter parameters. Available parameters include:
                - archived (bool): Include archived tasks (true) or only active tasks (false)
                - page (int): Page number of results (for pagination)
                - order_by (str): Field to order results by (e.g., "created", "updated", "due_date")
                - reverse (bool): Reverse order of results (true for descending)
                - subtasks (bool): Include subtasks (true) or exclude them (false)
                - statuses (list): Array of status names to filter tasks by
                - include_closed (bool): Include closed tasks (true) or exclude them (false)
                - assignees (list): Array of assignee user IDs to filter tasks by
                - due_date_gt (int): Filter for tasks with due date greater than timestamp (in milliseconds)
                - due_date_lt (int): Filter for tasks with due date less than timestamp (in milliseconds)
                - date_created_gt (int): Filter for tasks created after timestamp (in milliseconds)
                - date_created_lt (int): Filter for tasks created before timestamp (in milliseconds)
                - date_updated_gt (int): Filter for tasks updated after timestamp (in milliseconds)
                - date_updated_lt (int): Filter for tasks updated before timestamp (in milliseconds)
                - custom_fields (list): Array of custom field filter objects

        Returns:
            list: A list of Task objects.
        """
        from clickup_python_sdk.clickupobjects.task import Task

        # this will work for now but I need to eventually include paging at the api instead
        finished_iteration = False
        result = []
        page = 0

        route = self.get_endpoint() + "/task?"
        method = "GET"
        if params:
            for key, value in params.items():
                route += "&" + key + "=" + value

        while not finished_iteration:
            response = self.api.make_request(
                method=method, route=route + f"&page={page}"
            )
            if len(response["tasks"]) == 0:
                finished_iteration = True
                break
            for task in response["tasks"]:
                result.append(Task.create_object(data=task, target_class=Task))
            page += 1
        return result

    def create_task(
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
        parent=None,
        links_to=None,
        check_required_custom_fields=None,
        custom_fields=None,
    ):
        """
        Create a new task in this list.

        Args:
            name (str): Name of the task (required).
            description (str, optional): Description of the task.
            markdown_description (str, optional): Description of the task in markdown format.
                If both description and markdown_description are provided, markdown_description
                will be used.
            assignees (list, optional): Array of user IDs to assign to the task.
            tags (list, optional): Array of tag names to apply to the task.
            status (str, optional): Status of the task. Must be a valid status name for the list.
            priority (int, optional): Priority of the task (1-4, with 1 being highest).
            due_date (int, optional): Due date as a Unix timestamp in milliseconds.
            due_date_time (bool, optional): Whether the due date includes a time component.
            time_estimate (int, optional): Time estimate in milliseconds.
            start_date (int, optional): Start date as a Unix timestamp in milliseconds.
            start_date_time (bool, optional): Whether the start date includes a time component.
            notify_all (bool, optional): Whether to notify all assignees of the task creation.
            parent (str, optional): Task ID to create this task as a subtask of.
            links_to (str, optional): Task ID to link this task to.
            check_required_custom_fields (bool, optional): Whether to validate that all required
                custom fields are provided.
            custom_fields (list, optional): Array of custom field objects with format:
                [{"id": "custom_field_id", "value": field_value}]

        Returns:
            Task: The created Task object.

        Example:
            list.create_task(
                name="New Task",
                description="Task description",
                assignees=[123456, 789012],
                status="in progress",
                priority=2
            )
        """
        from clickup_python_sdk.clickupobjects.task import Task

        route = self.get_endpoint() + "/task"
        method = "POST"
        values = {"name": name}  # Name is required

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
        if parent is not None:
            values["parent"] = parent
        if links_to is not None:
            values["links_to"] = links_to
        if check_required_custom_fields is not None:
            values["check_required_custom_fields"] = check_required_custom_fields
        if custom_fields is not None:
            values["custom_fields"] = custom_fields

        response = self.api.make_request(method=method, route=route, values=values)
        return Task.create_object(data=response, target_class=Task)

    def get_custom_fields(self):
        """
        Get custom fields associated with this list.

        Retrieves all custom fields configured for the list.

        Returns:
            list: A list of CustomField objects.
        """
        from clickup_python_sdk.clickupobjects.customfield import CustomField

        route = self.get_endpoint() + "/field"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        result = []
        for field in response["fields"]:
            result.append(
                CustomField.create_object(data=field, target_class=CustomField)
            )
        return result

    def create_custom_field(
        self, field_name, type_name, type_config=None, required=False
    ):
        """
        Create a new custom field for this list.

        Args:
            field_name (str): Name of the custom field.
            type_name (str): Type of the custom field (e.g., "text", "dropdown", "checkbox", etc.).
            type_config (dict, optional): Configuration for the custom field type.
                Format depends on the field type. Refer to the ClickUp API documentation.
            required (bool, optional): Whether the field is required. Defaults to False.

        Returns:
            CustomField: The created CustomField object.
        """
        from clickup_python_sdk.clickupobjects.customfield import CustomField

        route = self.get_endpoint() + "/field"
        method = "POST"
        values = {
            "field_name": field_name,
            "type_name": type_name,
            "required": required,
        }

        if type_config is not None:
            values["type_config"] = type_config

        response = self.api.make_request(method=method, route=route, values=values)
        return CustomField.create_object(data=response, target_class=CustomField)

    def get_users(self):
        """
        Get users associated with this list.

        Retrieves all users that have access to this list.

        Returns:
            list: A list of User objects.
        """
        from clickup_python_sdk.clickupobjects.user import User

        route = self.get_endpoint() + "/member"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        result = []
        for member in response["members"]:
            result.append(User.create_object(data=member, target_class=User))
        return result

    def get_views(self):
        """
        Get views associated with this list.

        Retrieves all views configured for this list.

        Returns:
            list: A list of View objects.
        """
        from clickup_python_sdk.clickupobjects.view import View
        
        route = self.get_endpoint() + "/view"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        result = []
        for view in response.get("views", []):
            result.append(View.create_object(data=view, target_class=View))
        return result

    def create_view(
        self,
        name,
        type=None,
        content=None,
        parent=None,
        grouping=None,
        filtering=None,
        sorting=None,
        settings=None,
    ):
        """
        Create a new view for this list.

        Args:
            name (str): Name of the view.
            type (str, optional): Type of view (e.g., "list", "board", "calendar", etc.)
            content (str, optional): Description or content of the view.
            parent (str, optional): Parent view ID.
            grouping (dict, optional): Grouping configuration for the view.
            filtering (dict, optional): Filtering configuration for the view.
            sorting (dict, optional): Sorting configuration for the view.
            settings (dict, optional): Additional settings for the view.

        Returns:
            View: The created View object.
        """
        from clickup_python_sdk.clickupobjects.view import View
        
        route = self.get_endpoint() + "/view"
        method = "POST"
        values = {"name": name}

        if type is not None:
            values["type"] = type
        if content is not None:
            values["content"] = content
        if parent is not None:
            values["parent"] = parent
        if grouping is not None:
            values["grouping"] = grouping
        if filtering is not None:
            values["filtering"] = filtering
        if sorting is not None:
            values["sorting"] = sorting
        if settings is not None:
            values["settings"] = settings

        response = self.api.make_request(method=method, route=route, values=values)
        return View.create_object(data=response, target_class=View)
        
    def create_document(self, workspace_id, name, visibility=None, create_page=True):
        """
        Create a new Doc with this List as the parent.

        Args:
            workspace_id (str): The ID of the workspace where the document will be created (required).
            name (str): The name of the new Doc.
            visibility (str, optional): The visibility of the new Doc. For example, 'PUBLIC' or 'PRIVATE'.
            create_page (bool, optional): Whether to create a new page when creating the Doc. Defaults to True.

        Returns:
            Document: The created Document object.
        """
        from clickup_python_sdk.clickupobjects.document import Document

        route = f"workspaces/{workspace_id}/docs"
        method = "POST"
        values = {
            "name": name,
            "parent": {
                "id": self["id"],
                "type": 6  # 6 is the type for List
            },
            "create_page": create_page
        }

        if visibility is not None:
            values["visibility"] = visibility

        response = self.api.make_request(method=method, route=route, values=values, api_version="v3")
        
        new_document = Document(id=response.get("id"), workspace_id=workspace_id)
        new_document._set_data(response)
        return new_document