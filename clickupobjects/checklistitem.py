from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class ChecklistItem(AbstractObject):
    """
    Represents a ClickUp Checklist Item object.

    This class provides methods to interact with checklist items, including
    updating and removing checklist items.
    """

    def __init__(self, id=None, checklist_id=None) -> None:
        """
        Initialize a ChecklistItem object.

        Args:
            id (str, optional): The unique identifier of the checklist item. Defaults to None.
            checklist_id (str, optional): The ID of the parent checklist. Defaults to None.
        """
        super().__init__(id=id)
        self._checklist_id = checklist_id

    @property
    def checklist_id(self):
        """
        Get the ID of the parent checklist.

        Returns:
            str: The parent checklist ID.
        
        Raises:
            ValueError: If the checklist ID is not set.
        """
        if not self._checklist_id and 'checklist' in self and self['checklist']:
            self._checklist_id = self['checklist']['id']
            
        if not self._checklist_id:
            raise ValueError("Checklist ID is not set.")
            
        return self._checklist_id

    def get_endpoint(self):
        """
        Get the API endpoint for this checklist item.

        Returns:
            str: The API endpoint path for this checklist item.

        Raises:
            ValueError: If the checklist item ID or checklist ID is not set.
        """
        if "id" not in self:
            raise ValueError("Checklist item ID is not set.")
            
        return f"checklist/{self.checklist_id}/checklist_item/{self['id']}"
        
    def update(self, name=None, resolved=None, assignee=None, parent=None):
        """
        Update a checklist item.
        
        Args:
            name (str, optional): New name for the checklist item.
            resolved (bool, optional): Whether the item is checked/resolved.
            assignee (int, optional): User ID to assign the checklist item to.
            parent (str, optional): Parent checklist item ID for nested items.
            
        Returns:
            ChecklistItem: The current checklist item instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {}
        
        if name is not None:
            values["name"] = name
            
        if resolved is not None:
            values["resolved"] = resolved
            
        if assignee is not None:
            values["assignee"] = assignee
            
        if parent is not None:
            values["parent"] = parent
            
        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self
        
    def delete(self):
        """
        Delete a checklist item.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)
