import bcrypt


def get_password_hash(password: str) -> str:
    """
    Get password hash.

    :return: hash of password.
    """

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password=password_bytes,
        salt=salt,
    ).decode("utf-8")

    return hashed_password
