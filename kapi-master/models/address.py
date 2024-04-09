import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, String


class Address(Base):
    __tablename__ = "address"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    address = Column(String(255))
    zip_code = Column(String(10))
    city = Column(String)  # aka "Localidade"
    district = Column(String(255))
    region = Column(String)
    country = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)
