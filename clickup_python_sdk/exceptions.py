import json
import re


class ClickupError(Exception):
    pass


class ClickupRequestException(ClickupError):
    def __init__(self, message, request_context, http_status, http_headers, body):
        self._message = message
        self._request_context = request_context
        self._http_status = http_status
        self._http_headers = http_headers
        try:
            self._body = json.loads(body)
        except (TypeError, ValueError):
            self._body = body

        super().__init__(
            "\n\n"
            + "  Message: %s\n" % self._message
            + "  Method:  %s\n" % self._request_context.get("method")
            + "  Path:    %s\n" % self._request_context.get("route", "/")
            + "  Params:  %s\n" % self._request_context.get("params")
            + "\n"
            + "  Status:  %s\n" % self._http_status
            + "  Response:\n    %s"
            % re.sub(r"\n", "\n    ", json.dumps(self._body, indent=2))
            + "\n"
        )

    def message(self):
        return self._message

    def request_context(self):
        return self._request_context

    def http_status(self):
        return self._http_status

    def http_headers(self):
        return self._http_headers

    def body(self):
        return self._body
