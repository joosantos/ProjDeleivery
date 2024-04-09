from .base_model import BaseModel as Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("User", back_populates="user_role", uselist=False)
