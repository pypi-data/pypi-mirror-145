# py-assembly-payments
Unofficial Python client for the Assembly Payments API

## 🚧 In Development 🚧
This package is still undergoing development and is pre-v1. It currently implements around 30% of the Assembly Payments API. You can keep up with the [coverage here](https://github.com/divipayhq/py-assembly-payments/projects/1)

## Installation
```
pip install py-assembly-payments
```

## Example
```python
from assembly_payments.client import AssemblyClient

client = AssemblyClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# List Users
client.users.list()

# Create User
user = client.users.create(
    id="your-user-id",
    first_name="Jane",
    last_name="Doe",
    email="jane.doe@example.com"
)

# Easy object access
print(user.first_name + user.last_name) # Jane Doe
```

## Credentials
You can set your auth credentials in two ways:

1. Through arguments to the client:
```python
AssemblyClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=CLIENT_SCOPE, grant_type="client_credentials")
```

2. Through environment variable which `AssemblyClient` will pick up from:

```bash
export ASSEMBLY_CLIENT_ID=my-client-id
export ASSEMBLY_CLIENT_SECRET=my-client-secret
export ASSEMBLY_SCOPE=my-scope
```

`grant_type` defaults to `"client_credentials"` and can only be controlled by an argument to `AssemblyClient`.
