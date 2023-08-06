# Example

Building a simple Client is easy with the OBQLClient class.

- The first argument is the URL of the GraphQL server (which supports websocket transport and subscription).

```python
import time
from ob_graphql import OBQLClient


client = OBQLClient('ws://localhost:9001')
```

- Create a Simple GraphQL query

```python
query = """
query getUser($userId: Int!) {
  users (id: $userId) {
    id
    username
  }
}
"""
```

- This is a blocking call, you receive response in the `res` variable

```python
print('Making a query first')
res = client.query(query, variables={'userId': 2})
print('query result', res)
```

- Create a Subscription query

```python
subscription_query = """
subscription getUser {
  users (id: 2) {
    id
    username
  }
}
"""
```

- Our callback function, which will be called and passed data every time new data is available

```python
def my_callback(op_id, data):
    print(f"Got data for Operation ID: {op_id}. Data: {data}")

print('Making a graphql subscription now...')
sub_id = client.subscribe(subscription_query, callback=my_callback)
print('Created subscription and waiting. Callback function is called whenever there is new data')
```

- Do some operation while the subscription is running

```python
time.sleep(10)
client.stop_subscribe(sub_id)
client.close()
```
