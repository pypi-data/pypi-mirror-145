# fastapi_resource
Resource init and shutdown for FastAPI


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
