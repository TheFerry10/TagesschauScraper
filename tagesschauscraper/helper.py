import hashlib
import json
import os
from datetime import date, datetime
from typing import Union

from tagesschauscraper import constants


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

    def __init__(
        self,
        date_: date,
        date_pattern: str = "%Y/%m",
        data_dir: str = constants.data_dir,
    ) -> None:
        """
        Initialize parameters and make the directory tree.

        Parameters
        ----------
        date_ : date, Provided date object
        date_pattern : str, optional
            The date pattern describes the directory structure, by default "%Y/%m"
        data_dir : str, optional
            The base directory where the directory tree will be generated, by default constants.data_dir
        """
        self.date_ = date_
        self.make_dir_tree_from_date(date_pattern, data_dir)

    def make_dir_tree_from_date(
        self, date_pattern: str = "%Y/%m", data_dir: str = constants.data_dir
    ) -> None:
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


def create_file_name_from_date(
    date_or_datetime: Union[date, datetime],
    date_pattern: Union[str, None] = None,
    prefix: str = "",
    suffix: str = "",
    extension="",
) -> str:
    """
    Create a file name from a date object.

    Parameters
    ----------
    date_ : Union[date, datetime]
        Provided date or datetime object.
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
    if date_pattern is None:
        if isinstance(date_or_datetime, datetime):
            formatted_date = date_or_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            formatted_date = date_or_datetime.strftime("%Y-%m-%d")
    else:
        formatted_date = date_or_datetime.strftime(date_pattern)
    file_name = prefix + formatted_date + suffix + extension
    return file_name


def save_to_json(obj_: dict, file_path):
    with open(file_path, "w") as fp:
        json.dump(obj_, fp, indent=4)
    print(f"Saved to: {file_path}")
