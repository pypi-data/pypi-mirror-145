"""
Data Storage and Retrieval from JSON objects with ID's
"""
from pathlib import Path
import logging
try:
    import ujson as json
except ImportError:  # Fall back
    logging.warning("`ujson` package is not installed large JSON objects will be accessed/modified slower")
    import json # Fallback incase ujson isn't installed

class Reader:
    def __init__(self, directory: str, ids: list = list()) -> None:
        if not (Path(directory).exists() and Path(directory).is_dir()): # Check if that directory exists
            Path(directory).mkdir(parents=True) # Create the directories if needed
        self.directory = directory # Once verified make our directory pointer
        if not isinstance(ids, list):
            ids = list(ids) # Convert if its not a list
        self._ids = ids
        self.__defaults = {} # Stores the default values for each key to fix incase of missing keys

    def _repair_id(self, id, key):
        """
        Inits a ID in a key with the default value
        """
        self._file_check(key)
        id = str(id)
        self.write_file(id, key, self.__defaults[key]) # Write default value to ID
        logging.warning(f'Repaired {id} for key {key} succesfully')
        return self.__defaults[key]

    def _file_check(self, key):
        if not Path(f'{self.directory}/data_{key}.json').is_file():
            raise FileNotFoundError(f'{self.directory}/data_{key}.json does not exist')
        return True

    def update_ids(self, ids: list):
        """
        Overwrite ID list
            Parameters:
                ids (list): list to overwrite with
            Raises:
                SyntaxError if not list
        """
        if isinstance(ids, list):
            self._ids = ids # Update ID list
        else:
            raise SyntaxError(f"Expected `list` got {type(ids)}")

    def add_ids(self, ids: list):
        """
        Adds specified IDs
            Parameters:
                ids (list): IDs to add
            Raises:
                SyntaxError if not list
        """
        if isinstance(ids, list):
            for _id in ids:
                self._ids.append(_id)
        else:
            raise SyntaxError(f"Expected `list` got {type(ids)}")

    def add_id(self, id):
        """
        Adds a specified ID
            Parameters:
                id (any): ID to add
        """
        self._ids.append(id)

    def remove_ids(self, ids):
        """
        Removes specified IDs
            Parameters:
                ids (list): IDs to remove
            Raises:
                SyntaxError if not list
        """
        if isinstance(ids, list):
            for _id in ids:
                self._ids.remove(_id)
        else:
            raise SyntaxError(f"Expected `list` got {type(ids)}")

    def remove_ids(self, id):
        """
        Removes a specified ID
            Parameters:
                id (any): ID to remove
        """
        self._ids.remove(id)

    def create_file(self, key: str, default = "", wipe: bool = False):
        """
        Creates a JSON config file for all ids it can see with a default
            Parameters:
                key (str): The `data_[key].json` to generate
                default (any): The value to put in as a placeholder
                wipe (bool): Wipe the files forcefully
        """
        self.__defaults[key] = default # Store what the default was so we can repair if a id is missing
        try:
            self._file_check(key)
            if not wipe: # allows for wiping of the config
                logging.info(f'Detected {key} but file exist and wipe flag is not set')
                return
        except FileNotFoundError:
            pass # We'll be creating the file

        data = {}

        for id in self._ids:
            _id = str(id) # Make sure its a str for consistency
            data[_id] = default # Init with default value

        with open(f'{self.directory}/data_{key}.json', 'w') as fileout:
            json.dump(data, fileout, indent=4)
        logging.debug(f'Created {key} using {default} as the default')

    def read_file(self, id, key: str):
        """
        Reads a JSON file given the ID to find and key to look in
            Parameters:
                id (str/int): the ID to return given key
                key (str): The key to look up
            Returns:
                data(any): The data for that key/id pair
        """
        self._file_check(key)
        data = {}
        id= str(id)

        with open(f'{self.directory}/data_{key}.json', 'r') as filein:
            data = json.load(filein)

        try:
            return data[id]
        except KeyError:
            logging.warning(f'Repairing {id} for key {key}')
            return self._repair_id(id, key)

    def write_file(self, id, key: str, value):
        """
        Writes data to a key JSON given a id
            Parameters:
                id (str/int): ID to write to
                key (str): The key to modify
                value (any): The value to write for that key/id pair
        """
        self._file_check(key)
        data = {}
        id = str(id)

        with open(f'{self.directory}/data_{key}.json', 'r+') as file:
            data = json.load(file)
            data[id] = value
            file.seek(0)
            file.truncate(0)
            json.dump(data, file, indent=4)

    def remove(self, id, key: str):
        """
        Removes a id from a given key
            Parameters:
                id (str/int): ID to remove
                key (str): The key to modify
        """
        self._file_check(key)
        data = {}
        id = str(id)

        with open(f'{self.directory}/data_{key}.json', 'r+') as file:
            data = json.load(file)
            data.pop(id)
            file.seek(0)
            file.truncate(0)
            json.dump(data, file, indent=4)

    def dump(self, key: str):
        """
        Dumps all the JSON given the key
            Parameters:
                key (str): The key to dump
            Returns:
                data (dict): The JSON data
        """
        self._file_check(key)
        data = {}

        with open(f'{self.directory}/data_{key}.json', 'r') as filein:
            data = json.load(filein)

        return data