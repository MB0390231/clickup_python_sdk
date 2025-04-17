from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class DocumentPage(AbstractObject):
    """
    Represents a ClickUp Document Page object.

    This class provides methods to interact with ClickUp document pages, including viewing,
    creating, and updating pages within a document.
    """

    def __init__(self, id=None, workspace_id=None, doc_id=None) -> None:
        """
        Initialize a DocumentPage object.

        Args:
            id (str, optional): The unique identifier of the document page. Defaults to None.
            workspace_id (str): The ID of the workspace this page belongs to.
            doc_id (str): The ID of the document this page belongs to.

        Raises:
            ValueError: If workspace_id or doc_id is not provided.
        """
        if workspace_id is None or doc_id is None:
            raise ValueError(
                "workspace_id and doc_id are required to initialize a DocumentPage"
            )

        super().__init__(id=id)
        self["workspace_id"] = workspace_id
        self["doc_id"] = doc_id

    def get_endpoint(self):
        """
        Get the API endpoint for this page.

        Returns:
            str: The API endpoint path for this page.

        Raises:
            ValueError: If the page ID is not set.
        """
        if "id" not in self:
            raise ValueError("Page ID is not set.")
        return f"workspaces/{self['workspace_id']}/docs/{self['doc_id']}/pages/{self['id']}"

    def get(self, content_format="text/md"):
        """
        Retrieve information about this page.

        Args:
            content_format (str, optional): The format to return the page content in.
                                          For example, `text/md` for markdown or `text/plain` for plain.
                                          Defaults to "text/md".

        Returns:
            DocumentPage: The current page instance with updated information.
        """
        route = self.get_endpoint()
        method = "GET"
        params = {"content_format": content_format}
        response = self.api.make_request(
            method=method, route=route, params=params, api_version="v3"
        )
        self._set_data(response)
        return self

    def update(
        self,
        name=None,
        sub_title=None,
        content=None,
        content_edit_mode="replace",
        content_format="text/md",
    ):
        """
        Edit this page.

        Args:
            name (str, optional): The updated name of the page. Defaults to None.
            sub_title (str, optional): The updated subtitle of the page. Defaults to None.
            content (str, optional): The updated content of the page. Defaults to None.
            content_edit_mode (str, optional): The strategy for updating content on the page.
                                            For example, `replace`, `append`, or `prepend`. Defaults to "replace".
            content_format (str, optional): The format the page content is in.
                                        For example, `text/md` for markdown and `text/plain` for plain. Defaults to "text/md".

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        route = self.get_endpoint()
        method = "PUT"

        values = {
            "content_edit_mode": content_edit_mode,
            "content_format": content_format,
        }

        if name is not None:
            values["name"] = name

        if sub_title is not None:
            values["sub_title"] = sub_title

        if content is not None:
            values["content"] = content

        # Make the update request
        response = self.api.make_request(
            method=method, route=route, values=values, api_version="v3"
        )
        return self
