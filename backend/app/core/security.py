import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()
password_hasher = PasswordHash.recommended()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise RuntimeError('JWT_SECRET_KEY måste anges i .env.')


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int, role: str) -> str:
    return jwt.encode({'sub': str(user_id), 'role': role, 'type': 'access', 'exp': datetime.now(UTC) + timedelta(minutes=30)}, JWT_SECRET_KEY, algorithm='HS256')


def decode_access_token(token: str) -> dict[str, object]:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
