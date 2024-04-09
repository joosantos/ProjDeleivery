import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel as Base
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .insurance import InsuranceStatusEnum


class Athlete(Base):
    __tablename__ = "athletes"
    _deep_hidden_fields = [
        "team.athletes",
        "athletes.insured_entity.athlete",
        "athletes.federation_requests.athlete",
        "insured_entity.athlete",
    ]
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(255), index=True)
    birthday = Column(DateTime)
    weight = Column(Float)
    is_male = Column(Boolean)
    is_adapted = Column(Boolean, default=False)
    notes = Column(String)
    profile_picture_url = Column(String)

    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    insured_entity_id = Column(UUID(as_uuid=True), ForeignKey("insured_entities.id"))
    belt_id = Column(UUID(as_uuid=True), ForeignKey("belts.id"))
    private_info_id = Column(UUID(as_uuid=True), ForeignKey("private_info.id"))
    address_id = Column(UUID(as_uuid=True), ForeignKey("address.id"))
    responsible_id = Column(UUID(as_uuid=True), ForeignKey("responsible.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(DateTime)

    team = relationship("Team", back_populates="athletes")
    insured_entity = relationship(
        "InsuredEntity",
        primaryjoin="Athlete.id==InsuredEntity.athlete_id",
        back_populates="athlete",
        uselist=False,
    )
    belt = relationship("Belt")
    private_info = relationship("PrivateInfo")
    address = relationship("Address")
    responsible = relationship("Responsible")
    user = relationship(
        "User",
        primaryjoin="Athlete.id==User.athlete_id",
        back_populates="athlete",
        uselist=False,
    )

    @property
    def federated_in_current_season(self) -> bool:
        current_year = datetime.datetime.now().year
        for insurance in self.insured_entity.insurances:
            if (
                insurance.start_date.year == current_year
                or insurance.end_date.year == current_year
            ) and insurance.status == InsuranceStatusEnum.accepted.value:
                return True
        return False
