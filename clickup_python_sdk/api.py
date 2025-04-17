import requests, time, sys, json
from clickup_python_sdk.config import API
from clickup_python_sdk.exceptions import ClickupRequestException


class ClickupClient(object):
    API = API

    def __init__(self) -> None:
        pass

    @classmethod
    def init(cls, user_token=None):
        assert user_token != None, "Must provide user token"
        cls._set_default_headers(user_token)
        api = cls()
        cls._set_default_api(api)
        api.set_token_user()

        return api

    @classmethod
    def _set_default_headers(cls, user_token):
        cls.DEFAULT_HEADERS = {
            "Authorization": f"{user_token}",
            "Content-Type": "application/json",
        }

    @classmethod
    def _set_default_api(cls, api):
        cls.DEFAULT_API = api

    @classmethod
    def get_default_api(cls):
        return cls.DEFAULT_API

    def set_token_user(self):
        """
        Sets the user associated with the authorization token.

        Returns:
        None
        """
        from clickup_python_sdk.clickupobjects.user import User

        route = "user"
        method = "GET"
        response = self.make_request(method=method, route=route)

        target_class = User
        self.TOKEN_USER = User.create_object(
            data=response["user"], target_class=target_class
        )
        return

    def make_request(
        self, method, route, params=None, values=None, file=None, api_version="v2"
    ):
        # handle rate limit
        if not params:
            params = {}
        url = self.API + api_version + "/" + route
        if method in ["GET", "DELETE"]:
            response = requests.request(
                url=url, method=method, headers=self.DEFAULT_HEADERS, params=params
            )
        elif method == "POST":
            if file:
                headers = {"Authorization": self.DEFAULT_HEADERS["Authorization"]}
                response = requests.post(url, files=file, headers=headers)
                return
            elif values is None:
                response = requests.post(url, headers=self.DEFAULT_HEADERS)
            else:
                response = requests.post(
                    url, data=json.dumps(values), headers=self.DEFAULT_HEADERS
                )
        elif method == "PUT":
            response = requests.put(
                url, data=json.dumps(values), headers=self.DEFAULT_HEADERS
            )
        else:
            raise ValueError("Invalid request method")

        self._update_rate_limits(response.headers)
        self._verify_response(response, method, url, params, self.DEFAULT_HEADERS)

        # Handle empty responses
        if not response.text:
            return None

        # Try to parse JSON, but don't fail if it's not JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            # If it's not JSON, return the raw text
            return response.text

    def refresh_rate_limit(self):
        """
        makes a get request to the authorized_user endpoint to refresh the rate limit
        """
        route = "user"
        method = "GET"
        _ = self.make_request(method=method, route=route)
        return self

    def _verify_response(self, response, method, route, params, headers):
        status_code = response.status_code
        if not 200 <= status_code < 300:
            print(route)
            raise ClickupRequestException(
                "Call to ClickUp API was unsuccessful.",
                request_context={
                    "method": method,
                    "route": route,
                    "params": params,
                    "headers": headers,
                },
                http_headers=response.headers,
                http_status=response.status_code,
                body=response.text,
            )
        return True

    def _update_rate_limits(self, headers):
        self.RATE_LIMIT_REMAINING = headers.get("X-RateLimit-Remaining")
        self.RATE_RESET = headers.get("X-RateLimit-Reset")
        return

    def _beauty_sleep(self, t):
        """
        Just a pretty way to countdown in the terminal
        t is an interger
        """
        for i in range(t, 0, -1):
            sys.stdout.write(str(i) + " ")
            sys.stdout.flush()
            time.sleep(1)
        print("")
        return

    def get_teams(self, fields=None):
        from clickup_python_sdk.clickupobjects.team import Team

        target_class = Team
        route = "team"
        method = "GET"
        response = self.make_request(method=method, route=route)
        result = []
        for teams in response["teams"]:
            result.append(Team.create_object(data=teams, target_class=target_class))
        return result

    def get_task(self, task_id=None, fields=None):
        if task_id is None:
            raise Exception("Must provide task id.")
        from clickup_python_sdk.clickupobjects.task import Task

        target_class = Task
        route = "task/" + task_id + "/?custom_task_ids=&team_id=&include_subtasks=true"
        method = "GET"
        response = self.make_request(method=method, route=route)
        return Task.create_object(data=response, target_class=target_class)
