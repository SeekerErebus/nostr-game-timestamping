import requests
import time
import sys
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class BitTimeStamp:
    """A bitcoin timestamp handler.

    Public Methods:
    - get_full_timestamp
    - get_normal_time
    - get_current_timestamp
    - get_current_hash
    """

    def __init__(
            self,
            max_retries: int = 3,
            timeout: int = 10
    ) -> None:
        self.__session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.__session.mount("http://", adapter)
        self.__session.mount("https://", adapter)
        self.__timeout = timeout

        self.__rest_api_base = "blockstream.info/api"
        try:
            self.__current_height = self.__get_current_block_height(max_retries=max_retries, first_run=True)
            self.__current_hash = self.__get_current_block_hash(max_retries=max_retries, first_run=True)
            self.__last_time = time.time()
        except Exception as e:
            print(f"Fatal Error: {e}")
            sys.exit(1)
    def __get_current_block_height(self, max_retries: int = 1, first_run: bool = False) -> int:
        url = f"{self.__rest_api_base}/blocks/tip/height"
        for attempt in range(max_retries):
            try:
                height_resp = self.__session.get(url, timeout=self.__timeout)
                height_resp.raise_for_status()
                return int(height_resp.json())
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                elif first_run:
                    raise
        return self.__current_height
    def __get_current_block_hash(self, max_retries: int = 1, first_run: bool = False) -> int:
        url = f"{self.__rest_api_base}/block-height/{self.__current_height}"
        for attempt in range(max_retries):
            try:
                hash_resp = self.__session.get(url, timeout=self.__timeout)
                hash_resp.raise_for_status()
                block_hash = hash_resp.json()
                return int(block_hash, 16)
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                elif first_run:
                    raise
        return self.__current_hash
    def __update(self) -> None:
        check_time = time.time()
        if check_time - self.__last_time >= 30:
            self.__last_time = check_time
            self.__current_height = self.__get_current_block_height()
            self.__current_hash = self.__get_current_block_hash()
    def get_full_timestamp(self) -> tuple[float,int,int]:
        """Get the Full timestamp

        Returns:
            A tuple containing the last update time, the current timestamp, and the current hash.
        """
        self.__update()
        return (self.__last_time, self.__current_height, self.__current_hash)
    def get_normal_time(self) -> float:
        """Get the last update time

        Returns:
            The last update time as a float.
        """
        self.__update()
        return self.__last_time
    def get_current_timestamp(self) -> int:
        """Get the current timestamp (latest block height)
        
        Returns:
            The current timestamp as an int.
        """
        self.__update()
        return self.__current_height
    def get_current_hash(self) -> int:
        """Get the current block hash.

        Returns:
            The hash of the current block as a base-16 int.
        """
        self.__update()
        return self.__current_hash
    
    
