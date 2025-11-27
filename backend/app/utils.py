import re

from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError

pwd_context = PasswordHash.recommended()


def sanitizar_name(username: str) -> str:
    username = username.lower()
    username = re.sub(r'[^a-z\s]', '', username)
    username = re.sub(r'\s+', ' ', username).strip()

    return username


def handle_integrity_error(error: IntegrityError) -> str:
    dicio = {
        'users_email_key': 'email já cadastrado',
        'users_cpf_key': 'cpf já cadastrado',
    }

    key = error.args[0].split('"')[1]

    return dicio[key]


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
