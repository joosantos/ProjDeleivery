import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship


class PrivateInfo(Base):
    __tablename__ = "private_info"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String(255), index=True)
    phone_number = Column(String(20))
    nationality = Column(String)
    natural_region = Column(String)
    natural_country = Column(String)
    gender_is_male = Column(String)
    nif = Column(String(20))
    federation_number = Column(Integer)
    federation_active = Column(Boolean, default=False)

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

    identification_document = relationship("IdentificationDocument")
