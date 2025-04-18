from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Space(AbstractObject):
    """
    Represents a ClickUp Space object.

    This class provides methods to interact with ClickUp spaces, including viewing, updating,
    and deleting spaces, as well as managing space-related operations such as folders,
    lists, tags, and views.

    In the ClickUp hierarchy, Spaces are the highest organizational level of your Workspace
    and hold all of your Folders and Lists. Some settings, like ClickApps, are implemented
    at the Space level.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Space object.

        Args:
            id (str, optional): The unique identifier of the space. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this space.

        Returns:
            str: The API endpoint path for this space.

        Raises:
            ValueError: If the space ID is not set.
        """
        if "id" not in self:
            raise ValueError("Space ID is not set.")
        return "space/" + self["id"]

    def get(self):
        """
        Retrieve information about this space.

        Fetches space details from the ClickUp API. You can only access spaces that
        you have permission to view.

        Returns:
            Space: The current space instance with updated space information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self

    def update(
        self,
        name=None,
        color=None,
        private=None,
        admin_can_manage=None,
        multiple_assignees=None,
        features=None,
    ):
        """
        Update space properties.

        Args:
            name (str, optional): The updated name of the space.
            color (str, optional): The updated color of the space (hex code).
            private (bool, optional): Whether the space is private.
            admin_can_manage (bool, optional): Whether admins can manage this space.
            multiple_assignees (bool, optional): Whether multiple assignees are allowed in this space.
            features (dict, optional): Configuration for space features. Example:
                {
                    "due_dates": {"enabled": True, "start_date": False, "remap_due_dates": True, "remap_closed_due_date": False},
                    "time_tracking": {"enabled": False},
                    "tags": {"enabled": True},
                    "time_estimates": {"enabled": True},
                    "checklists": {"enabled": True},
                    "custom_fields": {"enabled": True},
                    "remap_dependencies": {"enabled": True},
                    "dependency_warning": {"enabled": True},
                    "portfolios": {"enabled": True}
                }

        Returns:
            Space: The current space instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {}

        if name is not None:
            values["name"] = name
        if color is not None:
            values["color"] = color
        if private is not None:
            values["private"] = private
        if admin_can_manage is not None:
            values["admin_can_manage"] = admin_can_manage
        if multiple_assignees is not None:
            values["multiple_assignees"] = multiple_assignees
        if features is not None:
            values["features"] = features

        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the space.

        Permanently removes the space from the workspace. This will also delete all
        folders, lists, and tasks within this space.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def get_folders(self, archived=None):
        """
        Get folders within this space.

        Retrieves folders that are contained within this space.

        Args:
            archived (bool, optional): Whether to include archived folders.
                If None, both archived and non-archived folders are returned.
                If True, only archived folders are returned.
                If False, only non-archived folders are returned.

        Returns:
            list: A list of Folder objects.
        """
        from clickup_python_sdk.clickupobjects.folder import Folder

        route = self.get_endpoint() + "/folder"
        if archived is not None:
            route += f"?archived={str(archived).lower()}"

        method = "GET"
        query = self.api.make_request(method=method, route=route)
        return [
            AbstractObject.create_object(data=folder, target_class=Folder)
            for folder in query["folders"]
        ]

    def create_folder(self, name):
        """
        Create a new folder in this space.

        Args:
            name (str): Name of the folder.

        Returns:
            Folder: The created Folder object.
        """
        from clickup_python_sdk.clickupobjects.folder import Folder

        route = self.get_endpoint() + "/folder"
        method = "POST"
        values = {"name": name}

        response = self.api.make_request(method=method, route=route, values=values)

        new_folder = Folder()
        new_folder._set_data(response)
        return new_folder

    def get_lists(self, archived=None):
        """
        Get folderless lists within this space.

        Retrieves lists that are directly contained within this space (not in any folder).

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
        result = []
        for list_data in response.get("lists", []):
            result.append(List.create_object(data=list_data, target_class=List))
        return result

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
        Create a new folderless list in this space.

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

    def get_tags(self):
        """
        Get task tags available in this space.

        Retrieves all tags configured for the space.

        Returns:
            list: A list of Tag objects.
        """
        from clickup_python_sdk.clickupobjects.tags import Tag

        route = self.get_endpoint() + "/tag"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        result = []
        for tag_data in response.get("tags", []):
            result.append(Tag.create_object(data=tag_data, target_class=Tag))
        return result

    def create_tag(self, name, tag_bg=None, tag_fg=None):
        """
        Create a new task tag in this space.

        Args:
            name (str): Name of the tag.
            tag_bg (str, optional): Background color of the tag (hex code).
            tag_fg (str, optional): Foreground (text) color of the tag (hex code).

        Returns:
            Tag: The created Tag object.
        """
        from clickup_python_sdk.clickupobjects.tags import Tag

        values = {"tag": {"name": name}}

        if tag_bg is not None:
            values["tag"]["tag_bg"] = tag_bg
        if tag_fg is not None:
            values["tag"]["tag_fg"] = tag_fg

        route = self.get_endpoint() + "/tag"
        method = "POST"
        response = self.api.make_request(method=method, route=route, values=values)
        
        new_tag = Tag()
        new_tag._set_data(response)
        return new_tag

    def get_views(self):
        """
        Get views associated with this space.

        Retrieves all views configured for this space.

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
        Create a new view for this space.

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
        Create a new Doc with this Space as the parent.

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
                "type": 4  # 4 is the type for Space
            },
            "create_page": create_page
        }

        if visibility is not None:
            values["visibility"] = visibility

        response = self.api.make_request(method=method, route=route, values=values, api_version="v3")
        
        new_document = Document(id=response.get("id"), workspace_id=workspace_id)
        new_document._set_data(response)
        return new_document