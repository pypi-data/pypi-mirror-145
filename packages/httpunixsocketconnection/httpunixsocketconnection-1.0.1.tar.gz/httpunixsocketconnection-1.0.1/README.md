# HTTPUnixSocketConnection

Really small Python class that extends native http.client.HTTPConnection allowing sending HTTP requests to Unix Sockets

## Installation

### Poetry

```sh
poetry add httpunixsocketconnection
```

### pip

```sh
pip install httpunixsocketconnection
```

## Usage

Because the class base is `http.client.HTTPConnection`, the API is almost the same.
Only the constructor and `connect` method is different.
With the rest please follow [the official docs](https://docs.python.org/3.8/library/http.client.html#http.client.HTTPConnection).

```python
from httpunixsocketconnection import HTTPUnixSocketConnection

# Create a connection
conn = HTTPUnixSocketConnection(
    unix_socket="/var/run/some.unix.socket"
    # timeout=Like in HTTPConnection
    # blocksize=Like in HTTPConnection
)
```

### Example: Getting list of Docker Containers

```python
from httpunixsocketconnection import HTTPUnixSocketConnection

conn = HTTPUnixSocketConnection("/var/run/docker.sock")
conn.request("GET", "/containers/json")

res = conn.getresponse()
print(res.status, res.reason)

content = res.read().decode("utf-8")
print(content)
```
