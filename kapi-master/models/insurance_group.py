import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, String, DateTime


class InsuranceGroup(Base):
    __tablename__ = "insurance_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    description = Column(String(1024))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)
