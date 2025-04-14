from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Group(AbstractObject):
    """
    Represents a ClickUp User Group object.

    This class provides methods to interact with ClickUp user groups, including viewing, updating,
    and deleting groups.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Group object.

        Args:
            id (str, optional): The unique identifier of the group. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this group.

        Returns:
            str: The API endpoint path for this group.

        Raises:
            ValueError: If the group ID is not set.
        """
        if "id" not in self:
            raise ValueError("Group ID is not set.")
        return "group/" + self["id"]
