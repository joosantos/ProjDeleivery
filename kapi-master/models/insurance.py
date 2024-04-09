import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
import enum
from .base_model import BaseModel as Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class InsuranceStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    denied = "denied"
    cancelled = "cancelled"
    requested = "requested"
    other = "other"


class Insurance(Base):
    __tablename__ = "insurances"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(
        String(255),
        default=InsuranceStatusEnum.pending.value,
        nullable=False,
    )
    notes = Column(String(255))
    sub_team_group = Column(UUID(as_uuid=True), index=True, nullable=False)
    medical_exam_url = Column(String(255))
    payment_comprovative_url = Column(String(255))
    contract_url = Column(String(255))
    coach_certificate_url = Column(String(255))

    insured_entity_id = Column(UUID(as_uuid=True), ForeignKey("insured_entities.id"))
    insurance_type_id = Column(UUID(as_uuid=True), ForeignKey("insurance_types.id"))
    insurance_group_id = Column(UUID(as_uuid=True), ForeignKey("insurance_groups.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    insurance_type = relationship("InsuranceType")
    insurance_group = relationship("InsuranceGroup")
    insured_entity = relationship("InsuredEntity", back_populates="insurances")
