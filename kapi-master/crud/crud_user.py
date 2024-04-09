from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import (
    or_,
    and_,
    func,
    extract,
    select,
    case,
    literal_column,
    Text,
)
from crud.base import CRUDBase
from models import User, UserRole, Role
from schemas import UserCreate, UserUpdate, UserRegister, AthleteToAssociate
from core.utils import get_password_hash, verify_password
from core.utils import validate_uuid4
from core.utils import commit_to_bd
from sql_app import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, id: UUID4) -> User:
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            user = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Database Error")
        if user is None:
            raise HTTPException(404)
        return user

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        try:
            return db.query(self.model).filter(User.email == email).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def is_registered(self, db: Session, id: UUID4) -> Optional[bool]:
        if not validate_uuid4(id):
            return None
        try:
            return (
                db.query(self.model).filter(self.model.id == id).first().hashed_password
                is not None
            )
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_by_name(self, db: Session, name: str) -> Optional[User]:
        try:
            return db.query(self.model).filter(User.name == name).first()
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def get_all_not_verified(self, db: Session) -> List[User]:
        try:
            return (
                db.query(self.model)
                .filter(
                    and_(
                        or_(User.admin_verified == None, User.admin_verified == False),
                        User.is_active == True,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def get_all(
        self,
        db: Session,
        is_coach: bool | None,
        name: str | None,
        athlete_associated: bool | None,
        limit: int,
        skip: int,
    ) -> tuple[int, list[User]]:

        sql_string = select(User)
        if is_coach is not None:
            sql_string = (
                sql_string.join(UserRole)
                .join(Role)
                .filter(Role.name == "COACH" if is_coach else Role.name != "COACH")
            )
        if name:
            sql_string = sql_string.filter(
                User.name.ilike(f"%{name.strip().replace(' ', '%')}%")
            )
        if athlete_associated is not None:
            sql_string = sql_string.filter(
                User.athlete_id != None
                if athlete_associated
                else User.athlete_id == None
            )

        try:
            n_results = len(db.scalars(sql_string).all())
            sql_string = sql_string.order_by(User.name)
            if limit != -1:
                sql_string = sql_string.offset(skip).limit(limit)
            return n_results, db.scalars(sql_string).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(503, "Server Error")

    def get_active_coaches(self, db: Session) -> List[User]:
        try:
            return (
                db.query(self.model)
                .join(UserRole)
                .join(Role)
                .filter(Role.name == "COACH")
                .filter(self.model.admin_verified == True)
                .order_by(self.model.name.asc())
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            return []

    def register(self, db: Session, obj_in: UserRegister) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
        )

        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_data(
        self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        obj_data = UserUpdate(**db_obj.__dict__).dict(exclude_unset=True)

        if isinstance(obj_in, dict):
            update = obj_in
        else:
            update = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update:
                setattr(db_obj, field, update[field])
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_insured_entity(
        self, db: Session, db_obj: User, insured_entity_id: UUID4
    ) -> User:
        if not validate_uuid4(insured_entity_id):
            raise HTTPException(404)
        db_obj.insured_entity_id = insured_entity_id
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def update_password(self, db: Session, db_obj: User, pass_in: str) -> User:
        hashed_password = get_password_hash(pass_in)

        setattr(db_obj, "hashed_password", hashed_password)
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def associate_athlete(
        self, db: Session, db_obj: User, athlete_id: UUID4
    ) -> Optional[User]:
        if not validate_uuid4(athlete_id):
            raise HTTPException(404)
        if not db_obj:
            return None
        db_obj.athlete_id = athlete_id  # type: ignore
        db.add(db_obj)

        return commit_to_bd(session_db=db, db_obj=db_obj)


user = CRUDUser(User)
