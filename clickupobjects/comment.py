from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Comment(AbstractObject):
    """
    Represents a ClickUp Comment object.

    This class provides methods to interact with ClickUp comments, including viewing, updating,
    and deleting comments.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Comment object.

        Args:
            id (str, optional): The unique identifier of the comment. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this comment.

        Returns:
            str: The API endpoint path for this comment.

        Raises:
            ValueError: If the comment ID is not set.
        """
        if "id" not in self:
            raise ValueError("Comment ID is not set.")
        return "comment/" + self["id"]

    def get(self):
        """
        Retrieve information about this comment.

        Fetches comment details from the ClickUp API. You can only access comments that
        you have permission to view.

        Returns:
            Comment: The current comment instance with updated comment information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self

    def update(self, comment_text):
        """
        Update the comment text.

        Args:
            comment_text (str): The new text content of the comment.

        Returns:
            Comment: The current comment instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {"comment_text": comment_text}
        
        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the comment.

        Permanently removes the comment from ClickUp.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def add_reaction(self, reaction):
        """
        Add a reaction to the comment.

        Args:
            reaction (str): The emoji reaction to add.

        Returns:
            Comment: The current comment instance with updated information.
        """
        route = self.get_endpoint() + "/reaction"
        method = "POST"
        values = {"reaction": reaction}
        
        response = self.api.make_request(method=method, route=route, values=values)
        return self.get()  # Refresh comment data

    def remove_reaction(self, reaction):
        """
        Remove a reaction from the comment.

        Args:
            reaction (str): The emoji reaction to remove.

        Returns:
            Comment: The current comment instance with updated information.
        """
        route = self.get_endpoint() + "/reaction/" + reaction
        method = "DELETE"
        
        response = self.api.make_request(method=method, route=route)
        return self.get()  # Refresh comment data
