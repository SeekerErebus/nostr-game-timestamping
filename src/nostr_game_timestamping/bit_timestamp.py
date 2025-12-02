import requests
import time

class BitTimeStamp:
    """A bitcoin timestamp handler.

    Public Methods:
    - get_full_timestamp
    - get_normal_time
    - get_current_timestamp
    - get_current_hash
    """

    def __init__(self) -> None:
        self.__rest_api_base = "https://blockstream.info/api"
        self.__current_height = self.__get_current_block_height()
        self.__current_hash = self.__get_current_block_hash()
        self.__last_time = time.time()
    def __get_current_block_height(self) -> int:
        height_resp = requests.get(f"{self.__rest_api_base}/blocks/tip/height")
        return height_resp.json()
    def __get_current_block_hash(self) -> int:
        hash_resp = requests.get(f"{self.__rest_api_base}/block-height/{self.__current_height}")
        block_hash = hash_resp.json()
        return int(block_hash, 16)
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
        return self.__last_time
    def get_current_timestamp(self) -> int:
        """Get the current timestamp (latest block height)
        
        Returns:
            The current timestamp as an int.
        """
        return self.__current_height
    def get_current_hash(self) -> int:
        """Get the current block hash.

        Returns:
            The hash of the current block as a base-16 int.
        """
        return self.__current_hash
    
    
