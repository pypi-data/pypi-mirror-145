# PyEmer
Python API for Emercoin blockchain.

## Usage

```python
from pyemer import Emer

# Emer(user, password, host, port)
emer = Emer("emccoinrpc", "emcpassword")

emer.name_show("dns:flibusta.lib").record.value
emer.name_new("some:name", "some value", 365)
emer.name_new("some:name2", b"byte value", 365, emer.get_account_address())
emer.name_history("some:name")[0].tx.height
emer.get_names_by_type("dns")[0].record.name
emer.get_block_count()

# You can call RPC manually
emer.rpc_connection.signmessage(
    emer.rpc_connection.getaccountaddress(""),
    "some message"
)
```
