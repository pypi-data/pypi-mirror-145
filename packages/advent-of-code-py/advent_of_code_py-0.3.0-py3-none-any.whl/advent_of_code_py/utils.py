"""utility module used to find latest year and day for advent of code problems"""
import datetime

from dateutil.tz import gettz

EASTERN = gettz("America/New_York")


def get_current_year() -> int:
    """
    Get latest year of advent of code return old year if month is not December
    otherwise return current year
    """
    date_time = datetime.datetime.now(tz=EASTERN)
    if date_time.month < 12:
        return date_time.year - 1
    return date_time.year


def get_day() -> int:
    """Get latest day or set a latest day as 25 if this is not month of December"""
    date_time = datetime.datetime.now(tz=EASTERN)
    if date_time.month == 12:
        return min(date_time.day, 25)
    return 25
