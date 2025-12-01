from bitcoin.rpc import Proxy
from bitcoin.rpc import JSONRPCError


class BitTimeStamp:
    def __init__(self, service_url: str | None = None, timeout: int = 30) -> None:
        self.timeout = timeout
        self.service_url = service_url
        if self.service_url is None:
            self.is_local = True
        else:
            self.is_local = False
        self.__proxy = Proxy(
            service_url=self.service_url,
            timeout=self.timeout
        )