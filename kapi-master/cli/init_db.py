from sql_app import Session
from typing import Optional
import json
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from core.utils import get_password_hash
from models import (
    User,
    Role as RoleModel,
    Category,
    UserRole,
    InsuranceType,
    InsuredType,
    CategoryType,
    Belt,
)
from schemas import CategoryCreate, CategoryTypeCreate
from constants.roles import Role

"""
Script to initialize the Database
"""


def get_belt_by_name(db: Session, name: str) -> Optional[Belt]:
    try:
        return db.query(Belt).filter(Belt.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_belt(db: Session, obj_in: Belt) -> Belt:
    db.add(obj_in)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")
    db.refresh(obj_in)
    return obj_in


def get_insured_type_by_name(db: Session, name: str) -> Optional[InsuredType]:
    try:
        return db.query(InsuredType).filter(InsuredType.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_insured_type(db: Session, obj_in: InsuredType) -> InsuredType:
    db.add(obj_in)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")
    db.refresh(obj_in)
    return obj_in


def get_insurance_type_by_name(db: Session, name: str) -> Optional[InsuranceType]:
    try:
        return db.query(InsuranceType).filter(InsuranceType.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_insurance_type(db: Session, obj_in: InsuranceType) -> InsuranceType:
    db.add(obj_in)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")
    db.refresh(obj_in)
    return obj_in


def get_role_by_name(db: Session, name: str) -> Optional[RoleModel]:
    try:
        return db.query(RoleModel).filter(RoleModel.name == name).first()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_role(db: Session, obj_in: RoleModel) -> RoleModel:
    db.add(obj_in)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")
    db.refresh(obj_in)
    return obj_in


def get_category_type_by_name(db: Session, name: str) -> Optional[CategoryType]:
    try:
        return db.query(CategoryType).filter(CategoryType.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_category_type(db: Session, obj_in: CategoryTypeCreate) -> CategoryType:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = CategoryType(**obj_in_data)
    db.add(db_obj)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")

    db.refresh(db_obj)
    return db_obj


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    try:
        return db.query(Category).filter(Category.name == name).first()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")


def create_category(db: Session, obj_in: CategoryCreate) -> Category:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = Category(**obj_in_data)
    db.add(db_obj)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")

    db.refresh(db_obj)
    return db_obj


def populate_db(db: Session):
    print("\n=== Started init_db.py script ===\n")

    print("\n=== Creating Roles ===\n")

    coach_role = get_role_by_name(db=db, name=Role.COACH["name"])
    if not coach_role:
        coach_role_in = RoleModel(
            name=Role.COACH["name"], description=Role.COACH["description"]
        )
        role: RoleModel = create_role(db=db, obj_in=coach_role_in)
        print("Created " + role.name + " role")
    else:
        print("Role " + coach_role.name + " already in DB")

    area_role = get_role_by_name(db=db, name=Role.AREA["name"])
    if not area_role:
        area_role_in = RoleModel(
            name=Role.AREA["name"], description=Role.AREA["description"]
        )
        role: RoleModel = create_role(db=db, obj_in=area_role_in)
        print("Created " + role.name + " role")
    else:
        print("Role " + area_role.name + " already in DB")

    admin_role = get_role_by_name(db=db, name=Role.ADMIN["name"])
    if not admin_role:
        admin_role_in = RoleModel(
            name=Role.ADMIN["name"], description=Role.ADMIN["description"]
        )
        role: RoleModel = create_role(db=db, obj_in=admin_role_in)
        print("Created " + role.name + " role")
    else:
        print("Role " + admin_role.name + " already in DB")

    micro_role = get_role_by_name(db=db, name=Role.MICRO["name"])
    if not micro_role:
        micro_role_in = RoleModel(
            name=Role.MICRO["name"], description=Role.MICRO["description"]
        )
        role: RoleModel = create_role(db=db, obj_in=micro_role_in)
        print("Created " + role.name + " role")
    else:
        print("Role " + admin_role.name + " already in DB")

    podium_role = get_role_by_name(db=db, name=Role.PODIUM["name"])
    if not podium_role:
        podium_role_in = RoleModel(
            name=Role.PODIUM["name"], description=Role.PODIUM["description"]
        )
        role: RoleModel = create_role(db=db, obj_in=podium_role_in)
        print("Created " + role.name + " role")
    else:
        print("Role " + admin_role.name + " already in DB")

    print("\n=== Ended creating Roles ===\n")

    print("\n=== Creating Users ===\n")

    users = json.load(open("./constants/users.json", "r"))

    for user in users:
        user_to_add = User(
            hashed_password=get_password_hash(user["password"]),
            name=user["name"],
            email=user["name"],
            email_verified=True,
            admin_verified=True,
        )
        user_db = db.query(User).filter(User.name == user_to_add.name).first()
        if user_db is None:
            role_aux = None
            if user_to_add.name == "Admin":
                role_aux = get_role_by_name(db=db, name=Role.ADMIN["name"])
            elif "Area" in user_to_add.name:
                role_aux = get_role_by_name(db=db, name=Role.AREA["name"])
            elif user_to_add.name == "Podium":
                role_aux = get_role_by_name(db=db, name=Role.PODIUM["name"])
            elif user_to_add.name == "Microphone":
                role_aux = get_role_by_name(db=db, name=Role.MICRO["name"])

            if role_aux is None:
                raise HTTPException(status_code=404, detail="Role Not Found")
            db.add(user_to_add)
            try:
                db.commit()
            except:
                db.rollback()
                raise HTTPException(status_code=503, detail="Error writing to DB")
            db.refresh(user_to_add)
            db.add(UserRole(user_id=user_to_add.id, role_id=role_aux.id))
            try:
                db.commit()
            except:
                db.rollback()
                raise HTTPException(status_code=503, detail="Error writing to DB")

            print("Created user " + user_to_add.name + " with role " + role_aux.name)
        else:
            print("User " + user_to_add.name + " already in DB")

    print("\n=== Ended creating Users ===\n")

    print("\n=== Creating Category Types ===\n")
    category_types = json.load(open("./constants/category_types.json", "r"))
    for category_type in category_types:
        if get_category_type_by_name(db=db, name=category_type["name"]) is None:
            create_category_type(
                db=db,
                obj_in=CategoryTypeCreate(
                    name=category_type["name"],
                    description=category_type["description"],
                ),
            )
            print("Created category type " + category_type["name"])
        else:
            print("Category type " + category_type["name"] + " already in DB")

    print("\n=== Ended creating Category Types ===\n")

    category_type_tournament = get_category_type_by_name(db=db, name="Tournament")
    if category_type_tournament is None:
        print("\nAN UNEXPECTED ERROR OCCURRED\n")
        return
    category_type_one_against_all = get_category_type_by_name(
        db=db, name="One against all"
    )
    if category_type_one_against_all is None:
        print("\nAN UNEXPECTED ERROR OCCURRED\n")
        return

    print("\n=== Creating Categories ===\n")
    categories = json.load(open("./constants/categories.json", "r"))
    for category in categories:
        if get_category_by_name(db=db, name=category["name"]) is None:
            create_category(
                db=db,
                obj_in=CategoryCreate(
                    name=category["name"],
                    third_place=category["third_place"],
                    three_points=category["three_points"],
                    rounds=category["rounds"],
                    penalties=category["penalties"],
                    order=category["order"],
                    number_all_at_once=category["number_all_at_once"],
                    category_type_id=category_type_tournament.id
                    if category["category_type"] == "Tournament"
                    else category_type_one_against_all.id,
                ),
            )
            print("Created category " + category["name"])
        else:
            print("Category " + category["name"] + " already in DB")

    print("\n=== Ended creating Categories ===\n")

    print("\n=== Creating Insurance Types ===\n")
    insurance_types = json.load(open("./constants/insurance_types.json", "r"))

    for insurance_type in insurance_types:
        if get_insurance_type_by_name(db=db, name=insurance_type["name"]) is None:
            create_insurance_type(
                db=db,
                obj_in=InsuranceType(
                    name=insurance_type["name"],
                    description=insurance_type["description"],
                    fee=insurance_type["fee"],
                ),
            )
            print("Created insurance type " + insurance_type["name"])
        else:
            print("Insurance type " + insurance_type["name"] + " already in DB")

    print("\n=== Ended creating Insurance Types ===\n")

    print("\n=== Creating Insured Types ===\n")
    insured_types = json.load(open("./constants/insured_types.json", "r"))

    for insured_type in insured_types:
        if get_insured_type_by_name(db=db, name=insured_type["name"]) is None:
            create_insured_type(db=db, obj_in=InsuredType(name=insured_type["name"]))
            print("Created insured type " + insured_type["name"])
        else:
            print("Insured type " + insured_type["name"] + " already in DB")

    print("\n=== Ended creating Insured Types ===\n")

    print("\n=== Creating Belts ===\n")
    belts = json.load(open("./constants/belts.json", "r"))

    for belt in belts:
        if get_belt_by_name(db=db, name=belt["name"]) is None:
            create_belt(db=db, obj_in=Belt(name=belt["name"], order=belt["order"]))
            print("Created belt " + belt["name"])
        else:
            print("Belt " + belt["name"] + " already in DB")

    print("\n=== Ended creating Belts ===\n")

    print("=== Ended init_db.py script ===")
