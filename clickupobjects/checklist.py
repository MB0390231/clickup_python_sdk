from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject
from clickup_python_sdk.clickupobjects.checklistitem import ChecklistItem


class Checklist(AbstractObject):
    """
    Represents a ClickUp Checklist object.

    This class provides methods to interact with ClickUp checklists, including viewing, updating,
    and managing checklist items.
    """

    def __init__(self, id=None, task_id=None) -> None:
        """
        Initialize a Checklist object.

        Args:
            id (str, optional): The unique identifier of the checklist. Defaults to None.
            task_id (str, optional): The ID of the task this checklist belongs to. Defaults to None.
        """
        super().__init__(id=id)
        self._task_id = task_id

    @property
    def task_id(self):
        """
        Get the ID of the task this checklist belongs to.

        Returns:
            str: The task ID.
        
        Raises:
            ValueError: If the task ID is not set.
        """
        if not self._task_id and 'task' in self and self['task'] and 'id' in self['task']:
            self._task_id = self['task']['id']
            
        if not self._task_id:
            raise ValueError("Task ID is not set.")
            
        return self._task_id

    def get_endpoint(self):
        """
        Get the API endpoint for this checklist.

        Returns:
            str: The API endpoint path for this checklist.

        Raises:
            ValueError: If the checklist ID is not set.
        """
        if "id" not in self:
            raise ValueError("Checklist ID is not set.")
        return f"checklist/{self['id']}"

    def get(self):
        """
        Retrieve information about this checklist.

        Fetches checklist details from the ClickUp API. You can only access checklists that
        you have permission to view.

        Returns:
            Checklist: The current checklist instance with updated information.
        """
        from clickup_python_sdk.clickupobjects.task import Task
        
        # Checklists are usually retrieved through the task endpoint
        route = f"task/{self.task_id}/checklist"
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        
        # Find this checklist in the response
        for checklist_data in response.get("checklists", []):
            if checklist_data.get("id") == self["id"]:
                self._set_data(checklist_data)
                break
                
        return self

    def update(self, name=None, position=None):
        """
        Update checklist properties.

        Args:
            name (str, optional): The updated name of the checklist.
            position (int, optional): The updated position of the checklist.

        Returns:
            Checklist: The current checklist instance with updated information.
        """
        route = self.get_endpoint()
        method = "PUT"
        values = {}

        if name is not None:
            values["name"] = name
        if position is not None:
            values["position"] = position

        response = self.api.make_request(method=method, route=route, values=values)
        self._set_data(response)
        return self

    def delete(self):
        """
        Delete the checklist.

        Permanently removes the checklist from ClickUp.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def get_items(self):
        """
        Get all items in this checklist.

        Returns:
            list: A list of ChecklistItem objects.
        """
        # Refresh the checklist data to get the latest items
        self.get()
        
        result = []
        if "items" in self:
            for item_data in self["items"]:
                item = ChecklistItem.create_object(data=item_data, target_class=ChecklistItem)
                # Set the checklist_id for the item
                item._checklist_id = self["id"]
                result.append(item)
                
        return result

    def create_item(self, name, assignee=None, parent=None):
        """
        Create a new item in this checklist.
        
        Args:
            name (str): The name of the checklist item.
            assignee (int, optional): User ID to assign the checklist item to.
            parent (str, optional): Parent checklist item ID for nested items.
            
        Returns:
            ChecklistItem: The created ChecklistItem object.
        """
        route = f"{self.get_endpoint()}/checklist_item"
        method = "POST"
        values = {"name": name}
        
        if assignee is not None:
            values["assignee"] = assignee
            
        if parent is not None:
            values["parent"] = parent
            
        response = self.api.make_request(method=method, route=route, values=values)
        
        item = ChecklistItem.create_object(data=response, target_class=ChecklistItem)
        item._checklist_id = self["id"]
        return item
