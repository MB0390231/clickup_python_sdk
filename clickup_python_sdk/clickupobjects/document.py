from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject
from clickup_python_sdk.clickupobjects.documentpage import DocumentPage


class Document(AbstractObject):
    """
    Represents a ClickUp Document object.

    This class provides methods to interact with ClickUp documents, including viewing,
    searching, creating, updating, and deleting documents.
    """

    def __init__(self, id=None, workspace_id=None) -> None:
        """
        Initialize a Document object.

        Args:
            id (str, optional): The unique identifier of the document. Defaults to None.
            workspace_id (str): The ID of the workspace this document belongs to.

        Raises:
            ValueError: If workspace_id is not provided.
        """
        if workspace_id is None:
            raise ValueError("workspace_id is required to initialize a Document")

        super().__init__(id=id)
        self["workspace_id"] = workspace_id

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
        return f"workspaces/{self['workspace_id']}/docs/{self['id']}"

    def get(self):
        """
        Retrieve information about this document.

        Returns:
            Document: The current document instance with updated information.
        """
        route = self.get_endpoint()
        method = "GET"
        response = self.api.make_request(method=method, route=route, api_version="v3")
        self._set_data(response)
        return self

    def get_page_listing(self, max_page_depth=-1):
        """
        View the PageListing for a Doc.

        Args:
            max_page_depth (int, optional): The maximum depth to retrieve pages and subpages.
                                         A value less than 0 does not limit the depth. Defaults to -1.

        Returns:
            dict: The page listing data.
        """
        if "id" not in self:
            raise ValueError("Document ID is not set.")

        route = f"workspaces/{self['workspace_id']}/docs/{self['id']}/pageListing"
        method = "GET"
        params = {"max_page_depth": max_page_depth}
        response = self.api.make_request(
            method=method, route=route, params=params, api_version="v3"
        )
        return response

    def get_pages(self, max_page_depth=-1, content_format="text/md"):
        """
        View pages belonging to a Doc.

        Args:
            max_page_depth (int, optional): The maximum depth to retrieve pages and subpages.
                                         A value less than 0 does not limit the depth. Defaults to -1.
            content_format (str, optional): The format to return the page content in.
                                        For example, `text/md` for markdown or `text/plain` for plain. Defaults to "text/md".

        Returns:
            list: A list of DocumentPage objects.
        """
        if "id" not in self:
            raise ValueError("Document ID is not set.")

        route = f"workspaces/{self['workspace_id']}/docs/{self['id']}/pages"
        method = "GET"
        params = {"max_page_depth": max_page_depth, "content_format": content_format}
        response = self.api.make_request(
            method=method, route=route, params=params, api_version="v3"
        )

        result = []
        for page_data in response:
            page = DocumentPage(
                id=page_data.get("id"),
                workspace_id=self["workspace_id"],
                doc_id=self["id"],
            )
            page._set_data(page_data)
            result.append(page)

        return result

    def create_page(
        self,
        name=None,
        content=None,
        parent_page_id=None,
        sub_title=None,
        content_format="text/md",
    ):
        """
        Create a page in a Doc.

        Args:
            name (str): The name of the new page.
            content (str): The content of the new page.
            parent_page_id (str, optional): The ID of the parent page. If this is a root page in the Doc,
                                         `parent_page_id` will not be returned. Defaults to None.
            sub_title (str, optional): The subtitle of the new page. Defaults to None.
            content_format (str, optional): The format the page content is in.
                                        For example, `text/md` for markdown or `text/plain` for plain. Defaults to "text/md".

        Returns:
            DocumentPage: The newly created page.
        """
        if "id" not in self:
            raise ValueError("Document ID is not set.")

        route = f"workspaces/{self['workspace_id']}/docs/{self['id']}/pages"
        method = "POST"

        values = {"name": name, "content": content, "content_format": content_format}

        if parent_page_id:
            values["parent_page_id"] = parent_page_id

        if sub_title:
            values["sub_title"] = sub_title

        response = self.api.make_request(
            method=method, route=route, values=values, api_version="v3"
        )

        page = DocumentPage(
            id=response.get("id"), workspace_id=self["workspace_id"], doc_id=self["id"]
        )
        page._set_data(response)

        return page
