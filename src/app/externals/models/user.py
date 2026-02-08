# pylint: disable=W0223
# pylint: disable=R0901

import hashlib
import uuid
from datetime import datetime, timezone
from random import randint
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import EmailType

from src.app.externals.exceptions import PasswordIncorrectException
from src.app.externals.models.base import Base

if TYPE_CHECKING:
    from src.app.externals.models.category import Category
    from src.app.externals.models.transaction import Transaction


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class PasswordType(TypeDecorator):
    impl = String(255)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        salt = uuid.uuid4().hex
        iterations = randint(90000, 99999)
        password = self.hashed_password(value, salt, iterations)
        return f"{salt}-{iterations}-{password}"

    @staticmethod
    def hashed_password(password: str, salt, iterations) -> str:
        value_encode = password.encode()

        salt_encode = salt.encode()
        password = hashlib.pbkdf2_hmac(
            "sha256", value_encode, salt_encode, iterations
        ).hex()
        return password


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[EmailType] = mapped_column(
        EmailType, nullable=False, unique=True
    )
    password: Mapped[PasswordType] = mapped_column(PasswordType, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=utc_now
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category", back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={str(self.id)}, name={self.name}"

    @property
    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @property
    def password_salt(self):
        return self.password.split("-")[0]

    @property
    def password_interations(self):
        return int(self.password.split("-")[1])

    @property
    def password_hash(self):
        return self.password.split("-")[2]

    @staticmethod
    def hashed_password(password: str, salt, iterations) -> str:
        value_encode = password.encode()

        salt_encode = salt.encode()
        password = hashlib.pbkdf2_hmac(
            "sha256", value_encode, salt_encode, iterations
        ).hex()
        return password

    def validate_password(self, password):
        password_try = self.hashed_password(
            password, self.password_salt, self.password_interations
        )
        if not password_try == self.password_hash:
            raise PasswordIncorrectException("invalid_user_or_password_error")
        return True
