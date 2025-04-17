from clickup_python_sdk.clickupobjects.abstractobject import AbstractObject


class Team(AbstractObject):
    """
    Represents a ClickUp Team/Workspace object.

    In the ClickUp API, a "team" refers to a workspace. This class provides methods
    to interact with ClickUp workspaces and manage workspace-level operations.
    """

    def __init__(self, id=None) -> None:
        """
        Initialize a Team object.

        Args:
            id (str, optional): The unique identifier of the team/workspace. Defaults to None.
        """
        super().__init__(id=id)

    def get_endpoint(self):
        """
        Get the API endpoint for this team.

        Returns:
            str: The API endpoint path for this team.

        Raises:
            ValueError: If the team ID is not set.
        """
        if "id" not in self:
            raise ValueError("Team ID is not set.")
        return "team/" + self["id"]

    def get_spaces(self, fields=None):
        """
        Get spaces within this team/workspace.

        Args:
            fields (list, optional): List of fields to include in the response.

        Returns:
            list: A list of Space objects.
        """
        from clickup_python_sdk.clickupobjects.space import Space

        route = self.get_endpoint() + "/space?"
        method = "GET"
        response = self.api.make_request(method=method, route=route)

        result = []
        for space in response["spaces"]:
            result.append(Space.create_object(data=space, target_class=Space))
        return result

    def get_task_templates(self, page=0):
        """
        Get task templates within this team/workspace.

        Args:
            page (int, optional): Page number for pagination. Defaults to 0.

        Returns:
            list: A list of TaskTemplate objects.
        """
        from clickup_python_sdk.clickupobjects.tasktemplate import TaskTemplate

        route = self.get_endpoint() + "/taskTemplate"
        method = "GET"
        params = {"page": page}
        response = self.api.make_request(method=method, route=route, params=params)

        result = []
        for template in response.get("templates", []):
            result.append(
                TaskTemplate.create_object(data=template, target_class=TaskTemplate)
            )
        return result

    def get_groups(self):
        """
        Get user groups in this team/workspace.

        Returns:
            list: A list of Group objects.
        """
        from clickup_python_sdk.clickupobjects.group import Group

        route = self.get_endpoint() + "/group"
        method = "GET"
        response = self.api.make_request(method=method, route=route)

        result = []
        for group in response.get("groups", []):
            result.append(Group.create_object(data=group, target_class=Group))
        return result

    def create_group(self, name, members=None):
        """
        Create a new user group in this team/workspace.

        Args:
            name (str): The name of the user group.
            members (list, optional): List of user IDs to add to the group.

        Returns:
            Group: The created Group object.
        """
        from clickup_python_sdk.clickupobjects.group import Group

        route = self.get_endpoint() + "/group"
        method = "POST"
        values = {"name": name}

        if members is not None:
            values["members"] = members

        response = self.api.make_request(method=method, route=route, values=values)

        new_group = Group()
        new_group._set_data(response)
        return new_group

    def update_group(self, group_id, name=None, members_add=None, members_remove=None):
        """
        Update a user group in this team/workspace.

        Args:
            group_id (str): The ID of the user group to update.
            name (str, optional): The new name for the user group.
            members_add (list, optional): List of user IDs to add to the group.
            members_remove (list, optional): List of user IDs to remove from the group.

        Returns:
            Group: The updated Group object.
        """
        from clickup_python_sdk.clickupobjects.group import Group

        route = self.get_endpoint() + f"/group/{group_id}"
        method = "PUT"
        values = {}

        if name is not None:
            values["name"] = name

        # Handle members
        if members_add is not None or members_remove is not None:
            members = {}
            if members_add is not None:
                members["add"] = members_add
            if members_remove is not None:
                members["rem"] = members_remove
            if members:
                values["members"] = members

        response = self.api.make_request(method=method, route=route, values=values)

        updated_group = Group()
        updated_group._set_data(response)
        return updated_group

    def delete_group(self, group_id):
        """
        Delete a user group in this team/workspace.

        Args:
            group_id (str): The ID of the user group to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        route = self.get_endpoint() + f"/group/{group_id}"
        method = "DELETE"
        response = self.api.make_request(method=method, route=route)
        return response.get("success", False)

    def search_docs(
        self,
        creator=None,
        deleted=None,
        archived=None,
        parent_id=None,
        parent_type=None,
        limit=None,
        next_cursor=None,
        doc_id=None,
    ):
        """
        Search documents in this workspace/team.

        Args:
            creator (int, optional): Filter to docs created by user with given ID.
            deleted (bool, optional): Filter to return deleted docs (default: False).
            archived (bool, optional): Filter to return archived docs (default: False).
            parent_id (str, optional): Filter to children of parent doc with given ID.
            parent_type (str, optional): Filter to children of given parent type
                (e.g., 'SPACE', 'FOLDER', 'LIST', 'EVERYTHING', 'WORKSPACE').
            limit (int, optional): Maximum number of results per page (10-100, default: 50).
            next_cursor (str, optional): Cursor for the next page of results.
            doc_id (str, optional): Filter to a single doc with given ID.

        Returns:
            list: A list of Document objects matching the search criteria.
        """
        from clickup_python_sdk.clickupobjects.document import Document

        route = f"workspaces/{self['id']}/docs"
        query_params = []

        # Add query parameters if they are provided
        if doc_id is not None:
            query_params.append(f"id={doc_id}")
        if creator is not None:
            query_params.append(f"creator={creator}")
        if deleted is not None:
            query_params.append(f"deleted={str(deleted).lower()}")
        if archived is not None:
            query_params.append(f"archived={str(archived).lower()}")
        if parent_id is not None:
            query_params.append(f"parent_id={parent_id}")
        if parent_type is not None:
            query_params.append(f"parent_type={parent_type}")
        if limit is not None:
            query_params.append(f"limit={limit}")
        if next_cursor is not None:
            query_params.append(f"next_cursor={next_cursor}")

        if query_params:
            route += "?" + "&".join(query_params)

        method = "GET"
        response = self.api.make_request(method=method, route=route, api_version="v3")

        result = []
        for doc_data in response.get("docs", []):
            # Create Document with workspace_id
            doc = Document(id=doc_data.get("id"), workspace_id=self["id"])
            doc._set_data(doc_data)
            result.append(doc)

        return result

    @classmethod
    def get_authorized_teams(cls):
        """
        Get workspaces available to the authenticated user.

        Returns:
            list: A list of Team objects for all workspaces available to the authenticated user.
        """
        team_obj = cls()
        route = "team"
        method = "GET"
        response = team_obj.api.make_request(method=method, route=route)

        result = []
        for team in response.get("teams", []):
            result.append(cls.create_object(data=team, target_class=cls))
        return result
