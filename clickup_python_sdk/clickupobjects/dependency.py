from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Dependency(AbstractObject):
    """
    Represents a ClickUp Dependency object.

    This class provides methods to interact with ClickUp task dependencies.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Dependency object.

        Args:
            id (str, optional): The unique identifier of the dependency. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this dependency.

        Returns:
            str: The API endpoint path for this dependency.

        Raises:
            ValueError: If the dependency ID is not set.
        """
        if "id" not in self:
            raise ValueError("Dependency ID is not set.")
        return "dependency/" + self["id"]
