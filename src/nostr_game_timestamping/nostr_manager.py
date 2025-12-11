import asyncio
from nostr_sdk import Keys, Client, EventBuilder, NostrSigner, RelayUrl


class NostrManager:
    """
    A support class for managing the Nostr connection.
    """
    def __init__(self) -> None:
        self.keys = Keys.generate()
        self.signer = NostrSigner.keys(self.keys)
        self.client = Client(self.signer)

        
