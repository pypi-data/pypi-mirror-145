"""
This module provides an easy way to manage various resources
that require initialization and cleanup (DB connections etc)
in FastAPI apps. You can use any context manager or function
that can be decorated with @contextmanager to define such a resource.

Example:

```
@FastApiResource
def db_conn():
    conn = db_client.connect()
    try:
        yield conn
    finally:
        conn.close()

app = FastAPI()

db_conn.bind(app)

@app.get('/')
def get_from_db(db = Depends(db_conn)):
    ...
```
"""

from contextlib import contextmanager
from typing import Any, Callable, ContextManager, Union


class FastApiResource:
    def __init__(self, contextmgr: Union[ContextManager, Callable]):
        if not isinstance(contextmgr, ContextManager):
            contextmgr = contextmanager(contextmgr)()
        self.contextmgr = contextmgr
        self._resource = None

    def __startup(self):
        self._resource = self.contextmgr.__enter__()

    def __call__(self) -> Any:
        if self._resource is None:
            self.__startup()
        return self._resource

    def __shutdown(self):
        if self._resource is not None:
            self.contextmgr.__exit__(None, None, None)

    def bind(self, app):
        app.on_event("startup")(self.__startup)
        app.on_event("shutdown")(self.__shutdown)
