from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Folder(AbstractObject):
    """
    Represents a ClickUp Folder object.

    This class provides methods to interact with ClickUp folders, including viewing, updating,
    and deleting folders, as well as managing folder-related operations such as lists and views.

    In the ClickUp hierarchy, Folders are part of a Space, and they can contain Lists, which
    in turn contain Tasks.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Folder object.

        Args:
            id (str, optional): The unique identifier of the folder. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this folder.

        Returns:
            str: The API endpoint path for this folder.

        Raises:
            ValueError: If the folder ID is not set.
        """
        if "id" not in self:
            raise ValueError("Folder ID is not set.")
        return "folder/" + self["id"]

    def get(self):
        """
        Retrieve information about this folder.

        Fetches folder details from the ClickUp API. You can only access folders that
        you have permission to view.

        Returns:
            Folder: The current folder instance with updated folder information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self

    def update(self, name):
        """
        Update the folder name.

        Args:
            name (str): The new name for the folder.

        Returns:
            Folder: The current folder instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {"name": name}

        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the folder.

        Permanently removes the folder from the workspace. This will also delete all
        lists and tasks within this folder.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def get_lists(self, archived=None):
        """
        Get lists within this folder.

        Retrieves lists that are contained within this folder.

        Args:
            archived (bool, optional): Whether to include archived lists.
                If None, both archived and non-archived lists are returned.
                If True, only archived lists are returned.
                If False, only non-archived lists are returned.

        Returns:
            list: A list of List objects.
        """
        from clickup_python_sdk.clickupobjects.list import List

        route = self.get_endpoint() + "/list"
        if archived is not None:
            route += f"?archived={str(archived).lower()}"

        method = "GET"
        response = self.api.make_request(method=method, route=route)

        return [
            AbstractObject.create_object(data=l, target_class=List)
            for l in response["lists"]
        ]

    def create_list(
        self,
        name,
        content=None,
        due_date=None,
        due_date_time=None,
        priority=None,
        assignee=None,
        status=None,
    ):
        """
        Create a new list in this folder.

        Args:
            name (str): Name of the list.
            content (str, optional): Description or content of the list.
            due_date (int, optional): Due date as a Unix timestamp in milliseconds.
            due_date_time (bool, optional): Whether the due date includes a time component.
            priority (int, optional): Priority level (1-4, with 1 being highest).
            assignee (str, optional): User ID to assign to the list.
            status (str, optional): Status of the list.

        Returns:
            List: The created List object.
        """
        from clickup_python_sdk.clickupobjects.list import List

        route = self.get_endpoint() + "/list"
        method = "POST"
        values = {"name": name}

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

        new_list = List()
        new_list._set_data(response)
        return new_list

    def get_views(self):
        """
        Get views associated with this folder.

        Retrieves all views configured for this folder.

        Returns:
            list: A list of View objects.
        """
        from clickup_python_sdk.clickupobjects.view import View

        route = self.get_endpoint() + "/view"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        
        return [
            AbstractObject.create_object(data=v, target_class=View)
            for v in response.get("views", [])
        ]

    def create_view(
        self,
        name,
        type=None,
        parent=None,
        grouping=None,
        filtering=None,
        sorting=None,
        settings=None,
    ):
        """
        Create a new view for this folder.

        Args:
            name (str): Name of the view.
            type (str, optional): Type of view (e.g., "list", "board", "calendar", etc.)
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
        
        new_view = View()
        new_view._set_data(response)
        return new_view
        
    def create_document(self, workspace_id, name, visibility=None, create_page=True):
        """
        Create a new Doc with this Folder as the parent.

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
                "type": 5  # 5 is the type for Folder
            },
            "create_page": create_page
        }

        if visibility is not None:
            values["visibility"] = visibility

        response = self.api.make_request(method=method, route=route, values=values, api_version="v3")
        
        new_document = Document(id=response.get("id"), workspace_id=workspace_id)
        new_document._set_data(response)
        return new_document