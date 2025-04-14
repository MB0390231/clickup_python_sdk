from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Document(AbstractObject):
    """
    Represents a ClickUp Document object.
    
    This class provides methods to interact with ClickUp documents, including viewing, 
    searching, creating, updating, and deleting documents.
    """
    
    def __init__(self, id=None) -> None:
        """
        Initialize a Document object.
        
        Args:
            id (str, optional): The unique identifier of the document. Defaults to None.
        """
        super().__init__(id=id)
        
    def get_endpoint(self):
        """
        Get the API endpoint for this document.
        
        Returns:
            str: The API endpoint path for this document.
            
        Raises:
            ValueError: If the document ID is not set.
        """
        if "id" not in self:
            raise ValueError("Document ID is not set.")
        return "doc/" + self["id"]
        
    def get(self):
        """
        Retrieve information about this document.
        
        Returns:
            Document: The current document instance with updated information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route)
        self._set_data(response)
        return self
