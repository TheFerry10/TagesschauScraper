import hashlib
import os
from datetime import date, datetime, timedelta
from typing import Union


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


def get_hash_from_string(string: str) -> str:
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
        root_dir: str = ".",
    ) -> None:
        """
        Initialize parameters and make the directory tree.

        Parameters
        ----------
        date_ : date, Provided date object
        date_pattern : str, optional
            The date pattern describes the directory structure, by default
            "%Y/%m"
        root_dir : str, optional
            The base directory where the directory tree will be generated, by
            default current directory ('.').
        """
        self.date_pattern = date_pattern
        self.date_ = date_
        self.root_dir = root_dir

    def create_file_path_from_date(
        self,
        date_pattern: Union[str, None] = None,
        root_dir: Union[str, None] = None,
    ) -> str:
        """
        Create a hierarchical file path from the given date object without
        creating directories.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure.
            Default date pattern from class initialization will be used when no
            pattern is provided.
        root_dir : str, optional
            The base directory where the directory tree will be generated.
            Default root directory from class initialization will be used when
            no directory is provided.
        """
        if date_pattern is None:
            date_pattern = self.date_pattern
        if root_dir is None:
            root_dir = self.root_dir
        self.file_path = os.path.join(
            root_dir, self.date_.strftime(date_pattern)
        )
        return self.file_path

    def make_dir_tree_from_date(
        self,
        date_pattern: Union[str, None] = None,
        root_dir: Union[str, None] = None,
    ) -> None:
        """
        Make a hierarchical directory tree from the given date object.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure.
            Default date pattern from class initialization will be used when
            no pattern is provided.
        root_dir : str, optional
            The base directory where the directory tree will be generated.
            Default root directory from class initialization will be used when
            no directory is provided.
        """
        file_path = self.create_file_path_from_date(date_pattern, root_dir)
        self.make_dir_tree_from_file_path(file_path)

    def make_dir_tree_from_file_path(self, file_path: str) -> None:
        os.makedirs(file_path, exist_ok=True)


def create_file_name_from_date(
    date_or_datetime: Union[date, datetime],
    date_pattern: Union[str, None] = None,
    prefix: str = "",
    suffix: str = "",
    extension: str = "",
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


def get_date_range(start_date: date, end_date: date) -> list[date]:
    """
    Return a date range from start date (inclusive) to end date (exclusive)
    with an interval of 1 day.

    Parameters
    ----------
    start_date : date
        Start date (inclusive)
    end_date : date
        End date (exclusive)

    Returns
    -------
    list[date]
        List of dates

    Raises
    ------
    ValueError
        When end_date is before start_date
    """
    if end_date > start_date:
        days_between = (end_date - start_date).days
        return [
            start_date + timedelta(days=days) for days in range(days_between)
        ]
    else:
        raise ValueError("end_date must be after start_date.")
