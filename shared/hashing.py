import hashlib


def sha256_hash(data: bytes) -> str:
    """
    Generate SHA256 hash for given data (used for chunk IDs).
    """
    return hashlib.sha256(data).hexdigest()


def hash_string(value: str) -> str:
    """
    Hash a string value (used for audit chaining).
    """
    return hashlib.sha256(value.encode()).hexdigest()