import hashlib


def hash(text: str, n: int = 5) -> str:
    hash = hashlib.sha1(text.encode("UTF-8")).hexdigest()
    return hash[:n]
