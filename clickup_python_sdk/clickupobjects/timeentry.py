from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class TimeEntry(AbstractObject):
    """
    Represents a ClickUp Time Entry object.

    This class provides methods to interact with ClickUp time entries, including viewing, updating,
    and deleting time entries.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a TimeEntry object.

        Args:
            id (str, optional): The unique identifier of the time entry. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this time entry.

        Returns:
            str: The API endpoint path for this time entry.

        Raises:
            ValueError: If the time entry ID is not set.
        """
        if "id" not in self:
            raise ValueError("Time Entry ID is not set.")
        return "time_entry/" + self["id"]
