import logging
from cuscom.clients.base_client import Client, ClientException

log = logging.getLogger(__name__)


class TaskClientException(ClientException):
    def __init__(self, e: ClientException, message=None):
        message = message or f"Failure using task client [{e.status_code}]: {e.body}"
        super(TaskClientException, self).__init__(e.status_code, e.body, e.url, message)


class TaskClient(Client):
    def fetch_tasks(self, params, endpoint):
        try:
            return self.request(method="GET", endpoint=endpoint, params=params)
        except ClientException as exc:
            raise TaskClientException(exc)

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._base_url})>"
