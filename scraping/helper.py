import hashlib
import json
import os
from datetime import date

from scraping import constants


def transform_datetime_str(datetime_string: str) -> str:
    """
    Transform datetime string to "%Y-%m-%d %H:%M:00".

    Parameters
    ----------
    datetime_string : str
        Provided datetime string.

    Returns
    -------
    str
        Transformed datetime string
        
    Examples
    --------
    transform_datetime_str("30.01.2021 - 18:04 Uhr")
    >>> 2021-01-30 18:04:00
    transform_datetime_str("30.01.2021 -    20:04 Uhr")
    >>> 2021-01-30 20:04:00
    """    
    date, time = [x.strip() for x in datetime_string.split("-")]
    day, month, year = date.split(".")
    hour, minute = time.split(" ")[0].split(":")
    second = "00"
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def get_hash_from_string(string):
    result = hashlib.sha1(string.encode())
    return result.hexdigest()


class DateDirectoryTreeCreator:
    """
    Create a directory tree and file name based on a date object.
    """
    def __init__(self, date_:date, date_pattern: str="%Y/%m", data_dir: str=constants.data_dir) -> None:
        """
        Initialize parameters and make the directory tree.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure, by default "%Y/%m"
        data_dir : str, optional
            The base directory where the directory tree will be generated, by default constants.data_dir
        """
        self.date_ = date_
        self.file_path = None
        self.make_dir_tree_from_date(date_pattern, data_dir)

    def make_dir_tree_from_date(self, date_pattern: str="%Y/%m", data_dir: str=constants.data_dir) -> None:
        """
        Make a hirachical directory tree from the given date object.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure, by default "%Y/%m"
        data_dir : str, optional
            The base directory where the directory tree will be generated, by default constants.data_dir
        """
        self.path = os.path.join(data_dir, self.date_.strftime(date_pattern))
        os.makedirs(self.path, exist_ok=True)

    def create_file_name_from_date(self, date_pattern: str="%Y-%m-%d", prefix: str="", suffix: str="", extension="") -> str:
        """
        Create a file name from a date object.

        Parameters
        ----------
        date_pattern : str, optional
            Date pattern in file name, by default "%Y-%m-%d"
        prefix : str, optional
            String before date pattern, by default ""
        suffix : str, optional
            String after date pattern, by default ""
        extension : str, optional
            File extension including ., e.g. '.csv' or '.json', by default ""

        Returns
        -------
        str
        The full file name.
        """    
        file_name = prefix + self.date_.strftime(date_pattern) + suffix + extension
        return file_name
    
    def get_file_path_name(self, date_pattern: str="%Y-%m-%d", prefix: str="", suffix: str="", extension="") -> str:
        """
        Create a file path from a date object.

        Parameters
        ----------
        date_pattern : str, optional
            Date pattern in file name, by default "%Y-%m-%d"
        prefix : str, optional
            String before date pattern, by default ""
        suffix : str, optional
            String after date pattern, by default ""
        extension : str, optional
            File extension including ., e.g. '.csv' or '.json', by default ""

        Returns
        -------
        str
        The full file name.
        """    
        file_name = self.create_file_name_from_date(date_pattern=date_pattern, prefix=prefix, suffix=suffix, extension=extension)
        return os.path.join(self.path, file_name)
    
def save_to_json(obj_: dict, file_path):
    with open(file_path, "w") as fp:
        json.dump(obj_, fp, indent=4)
    print(f"Saved to: {file_path}")