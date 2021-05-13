from sqlalchemy import (Column, String)

from ._base_model import BaseModel, Base

STRING_SIZE = 64


class Account(BaseModel, Base):
    __tablename__ = "accounts"

    tenant_id = Column(String(STRING_SIZE), nullable=False, unique=True, index=True)
    name = Column(String(STRING_SIZE))
    email = Column(String(STRING_SIZE), nullable=False, unique=True, index=True)
    phone = Column(String(STRING_SIZE))
