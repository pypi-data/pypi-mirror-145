import re

from typing import Optional


ZOOM_LINK_PATTERN = re.compile(r"https://\w*.?zoom.us/j/\d+(\?pwd=\w+)?")


def contains_zoom_link(text: str) -> Optional[str]:
    m = ZOOM_LINK_PATTERN.search(text)
    if m:
        return m.group(0)

    return None
