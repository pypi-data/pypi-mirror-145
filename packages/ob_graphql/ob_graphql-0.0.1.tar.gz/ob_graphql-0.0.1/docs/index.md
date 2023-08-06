# Ob-Graphql

Setup a simple GraphQL client over websocket using [apollo-transport-ws](https://github.com/apollographql/subscriptions-transport-ws/blob/master/PROTOCOL.md) protocol.

## GraphQL over WebSocket Protocol

### Client-server communication

Each message has a `type` field, which defined in the protocol of this package, as well as associated fields inside `payload` field, depending on the message type, and `id` field so the client can identify each response from the server.

Each WebSocket message is represented in JSON structure, and being stringified before sending it over the network.

This is the structure of each message:

```typescript
export interface OperationMessage {
  payload?: any;
  id?: string;
  type: string;
}
```

## Install

```bash
pip install ob_graphql
```

- Ob-Graphql depends on [websocket-client](https://pypi.org/project/websocket-client/) is a WebSocket client for Python. It provides access to low level APIs for WebSockets.

## Examples

### Setup subscriptions super easily

```python
from ob_graphql import OBQLClient

query = """
  subscription {
    notifications {
      id
      title
      content
    }
  }
"""


def callback(_id, data):
    print("got new data..")
    print(f"msg id: {_id}. data: {data}")


with OBQLClient("ws://localhost:8080/graphql") as client:

    sub_id = client.subscribe(query, callback=callback)
    client.stop_subscribe(sub_id)
```

### Variables can be passed

```python
from ob_graphql import OBQLClient

query = """
    subscription ($limit: Int!) {
      notifications (order_by: {created: "desc"}, limit: $limit) {
        id
        title
        content
      }
    }
  """

def callback(_id, data):
     print("got new data..")
     print(f"msg id: {_id}. data: {data}")

with OBQLClient('ws://localhost:8080/graphql') as client:
  sub_id = client.subscribe(query, variables={'limit': 10}, callback=callback)

```

### Headers can be passed too

```python
from ob_graphql import OBQLClient

query = """
    subscription ($limit: Int!) {
      notifications (order_by: {created: "desc"}, limit: $limit) {
        id
        title
        content
      }
    }
  """


def callback(_id, data):
    print("got new data..")
    print(f"msg id: {_id}. data: {data}")


with OBQLClient("ws://localhost:8080/graphql") as client:
    sub_id = client.subscribe(
        query,
        variables={"limit": 10},
        headers={"Authorization": "Bearer xxxx"},
        callback=callback,
    )
    client.stop_subscribe(sub_id)
```

### Normal queries and mutations work too

```python
from ob_graphql import OBQLClient

query = """
  query ($limit: Int!) {
    notifications (order_by: {created: "desc"}, limit: $limit) {
      id
      title
      content
    }
  }
"""

with OBQLClient('ws://localhost:8080/graphql') as client:
    res = client.query(query, variables={'limit': 10}, headers={'Authorization': 'Bearer xxxx'})
    print(res)
```

### Without the context manager API

```python
from ob_graphql import OBQLClient

query = """
  query ($limit: Int!) {
    notifications (order_by: {created: "desc"}, limit: $limit) {
      id
      title
      content
    }
  }
"""

client = OBQLClient('ws://localhost:8080/graphql')
res = client.query(query, variables={'limit': 10}, headers={'Authorization': 'Bearer xxxx'})
print(res)
client.close()
```
