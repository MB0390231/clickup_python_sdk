from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class User(AbstractObject):
    """
    Represents a ClickUp User object.

    This class provides methods to interact with individual ClickUp users, 
    including viewing user information and retrieving user-specific data.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a User object.

        Args:
            id (str, optional): The unique identifier of the user. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this user.

        Returns:
            str: The API endpoint path for this user.

        Raises:
            ValueError: If the user ID is not set.
        """
        if "id" not in self:
            raise ValueError("User ID is not set.")
        return "user/" + self["id"]

    def get(self):
        """
        Retrieve information about the currently authenticated user.
        
        This endpoint does not require a user ID as it returns information about 
        the authenticated user based on the API token.

        Returns:
            User: The current user instance with updated user information.
        """
        route = "user"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self
        
    def get_workspace_user(self, team_id, user_id=None):
        """
        Get information about a specific user in a workspace.
        
        This endpoint is only available on Enterprise plans.
        
        Args:
            team_id (str): The ID of the workspace (team).
            user_id (str, optional): The ID of the user to retrieve. 
                If not provided, uses the current user's ID if available.
                
        Returns:
            User: A User object with information about the specified user.
        """
        if user_id is None:
            if "id" not in self:
                raise ValueError("User ID is not set and no user_id parameter provided.")
            user_id = self["id"]
            
        route = f"team/{team_id}/user/{user_id}"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        
        user_obj = User()
        user_obj._set_data(response)
        return user_obj
        
    @classmethod
    def get_authorized_user(cls):
        """
        Get information about the currently authenticated user.
        
        Returns:
            User: A User object with the authenticated user's information.
        """
        user_obj = cls()
        route = "user"
        method = "GET"
        response = user_obj.api.make_request(method=method, route=route)
        user_obj._set_data(response)
        return user_obj
