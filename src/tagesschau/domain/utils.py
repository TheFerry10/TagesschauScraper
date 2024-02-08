from datetime import date

from tagesschau.domain.constants import DEFAULT_DATE_PATTERN


def transform_date(
    date_: date, date_pattern: str = DEFAULT_DATE_PATTERN
) -> str:
    return date_.strftime(date_pattern)
