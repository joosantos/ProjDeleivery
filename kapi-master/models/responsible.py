import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship as re


class Responsible(Base):
    __tablename__ = "responsible"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255))
    relationship = Column(String(255))
    email = Column(String(255))

    identification_document_id = Column(
        UUID(as_uuid=True), ForeignKey("identification_document.id")
    )

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    identification_document = re("IdentificationDocument")
