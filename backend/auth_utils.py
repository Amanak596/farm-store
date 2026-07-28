"""
auth_utils.py
------------------------------------------------------------
Small helper functions for password security.
We never store plain text passwords - only a salted hash.
------------------------------------------------------------
"""

import hashlib
import secrets


def hash_password(password: str) -> str:
    """Creates a random salt + hashes the password with it."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Checks a login attempt against the stored 'salt$hash' value."""
    try:
        salt, hashed = stored_hash.split("$")
    except ValueError:
        return False
    attempt_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return secrets.compare_digest(attempt_hash, hashed)
