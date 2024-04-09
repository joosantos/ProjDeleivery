import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, String


class IdentificationDocument(Base):
    __tablename__ = "identification_document"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    type = Column(String)
    number = Column(String)
    emitted_by = Column(String)
    expiration_date = Column(DateTime)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)
