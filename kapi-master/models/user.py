import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    _deep_hidden_fields = [
        "user_role.user",
        "user_role.user",
    ]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    hashed_password = Column(String(255), nullable=True)
    email_verified = Column(Boolean(), default=False)
    admin_verified = Column(Boolean())
    is_active = Column(Boolean(), default=True)
    notes = Column(String)

    insured_entity_id = Column(UUID(as_uuid=True), ForeignKey("insured_entities.id"))
    private_info_id = Column(UUID(as_uuid=True), ForeignKey("private_info.id"))
    address_id = Column(UUID(as_uuid=True), ForeignKey("address.id"))
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athletes.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    user_role = relationship("UserRole", back_populates="user", uselist=False)
    teams = relationship(
        "Team",
        back_populates="coach",
        uselist=True,
        primaryjoin="User.id==Team.coach_id",
    )
    insured_entity = relationship(
        "InsuredEntity",
        primaryjoin="User.id==InsuredEntity.user_id",
        back_populates="user",
        uselist=False,
    )
    private_info = relationship("PrivateInfo")
    address = relationship("Address")
    athlete = relationship(
        "Athlete",
        primaryjoin="User.athlete_id==Athlete.id",
        back_populates="user",
        uselist=False,
    )
