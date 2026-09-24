from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
jwt_secret = "change-me-to-a-secret-key-32-chars"
jwt_algorithm = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_passsword: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_passsword, hashed_password)


def create_access_token(id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {"sub": str(id), "exp": expire}
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, jwt_secret, algorithm=[jwt_algorithm])
