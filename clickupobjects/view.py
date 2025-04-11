from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class View(AbstractObject):
    """
    Represents a ClickUp View object.

    This class provides methods to interact with ClickUp views, including viewing, updating,
    and managing view-related operations.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a View object.

        Args:
            id (str, optional): The unique identifier of the view. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this view.

        Returns:
            str: The API endpoint path for this view.

        Raises:
            ValueError: If the view ID is not set.
        """
        if "id" not in self:
            raise ValueError("View ID is not set.")
        return "view/" + self["id"]

    def get(self):
        """
        Retrieve information about this view.

        Fetches view details from the ClickUp API. You can only access views that
        you have permission to view.

        Returns:
            View: The current view instance with updated view information.
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
        type=None,
        parent=None,
        grouping=None,
        filtering=None,
        sorting=None,
        settings=None,
    ):
        """
        Update view properties.

        Args:
            name (str, optional): The updated name of the view.
            content (str, optional): The updated content/description of the view.
            type (str, optional): Type of view (e.g., "list", "board", "calendar", etc.).
            parent (str, optional): Parent view ID.
            grouping (dict, optional): Grouping configuration for the view.
            filtering (dict, optional): Filtering configuration for the view.
            sorting (dict, optional): Sorting configuration for the view.
            settings (dict, optional): Additional settings for the view.

        Returns:
            View: The current view instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {}

        if name is not None:
            values["name"] = name
        if content is not None:
            values["content"] = content
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
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the view.

        Permanently removes the view from ClickUp.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)
