from typing import Union


def month_normalizer(month: Union[str, int]) -> int:
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    if isinstance(month, str):
        month = month.title()[:3]
        if month in months:
            return months.index(month) + 1

        raise ValueError(
            f"Month: {month} is not valid. Provide an integer from 1 -> 12 or a name of a"
            " month."
        )

    return month
