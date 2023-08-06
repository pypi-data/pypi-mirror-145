import base64
from typing import Optional, Union

import pyemer.models as models
from pyemer.authproxy import AuthServiceProxy, JSONRPCException


class Emer:
    def __init__(self, user: str, password: str, host: str = "localhost", port: int = 6662):
        self.rpc_connection = AuthServiceProxy(f"http://{user}:{password}@{host}:{str(port)}")

    def get_block_count(self) -> int:
        return self.rpc_connection.getblockcount()

    def name_show(self, name: (str, models.NVSRecord), value_type: Optional[models.ValueType] = None) -> models.NVSTx:
        if isinstance(name, models.NVSRecord):
            name = name.name
        lst = [name]
        if value_type is not None:
            lst.append(value_type.value)
        r = self.rpc_connection.name_show(*lst)
        record = models.NVSRecord(name, base64.b64decode(r["value"]))
        tx = models.Transaction(r["txid"], r["time"])
        addr = models.EmcAddress(r["address"])
        return models.NVSTx(record, addr, tx)

    def name_filter(self, regexp: str) -> [models.NVSRecord]:
        r = self.rpc_connection.name_filter(regexp)
        resp: [models.NVSRecord] = []
        for i in r:
            resp.append(models.NVSRecord(name=i["name"], value=i["value"]))
        return resp

    def name_history(self, name: (str, models.NVSRecord)) -> [models.NVSTx]:
        if isinstance(name, models.NVSRecord):
            name = name.name
        r: [{}] = self.rpc_connection.name_history(name)
        ret: [models.NVSTx] = []
        for i in r:
            record = models.NVSRecord(name, i["value"])
            tx = models.Transaction(i["txid"], i["time"], i["height"])
            addr = models.EmcAddress(i["address"])
            days = i["days_added"]
            ret.append(models.NVSTx(record, addr, tx, days))
        return ret

    def get_names_by_type(self, record_type: str) -> [models.NVSTx]:
        i = self.name_filter(f"^{record_type}:")
        ret: [models.NVSTx] = []
        for n in i:
            try:
                ret.append(self.name_show(n))
            except JSONRPCException:
                continue
        return ret

    def get_names_by_regex(self, regex: str) -> [models.NVSTx]:
        i = self.name_filter(regex)
        ret: [models.NVSTx] = []
        for n in i:
            try:
                ret.append(self.name_show(n))
            except JSONRPCException:
                continue
        return ret

    def name_new(
        self,
        name: str,
        value: Union[str, bytes],
        days: int,
        to_address: Optional[models.EmcAddress] = None,
    ) -> None:
        lst = [name, value, days]
        if to_address is not None:
            if isinstance(value, bytes):
                lst = [name, base64.b64encode(value).decode(), days, to_address.address, "base64"]
            elif isinstance(value, str):
                lst = [name, value, days, to_address.address]
        self.rpc_connection.name_new(*lst)

    def name_delete(self, name: str) -> None:
        self.rpc_connection.name_delete(name)

    def get_account_address(self, account: str = "") -> models.EmcAddress:
        return models.EmcAddress(self.rpc_connection.getaccountaddress(account))

    def help(self) -> str:
        return self.rpc_connection.help()
