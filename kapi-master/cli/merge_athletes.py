from pydantic import UUID4
from typing import Any
from models import (
    Athlete,
    PrivateInfo,
    IdentificationDocument,
    Address,
    Responsible,
)
import sys

from sql_app import Session
from pydantic import parse_obj_as
import json

from schemas import AthleteAdmin

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/merge_athletes.py {FED_NUM}
Replace {FED_NUM} with the number of federation commum to the 2 athletes
"""


def main(db: Session):
    athlete_number = sys.argv[1:][0]

    athletes_models = (
        db.query(Athlete)
        .join(PrivateInfo)
        .filter(PrivateInfo.federation_number == athlete_number)
        .all()
    )
    if len(athletes_models) == 1:
        print("Only exists 1 athlete")
        return

    athletes = []
    # Garantee that merges only two
    max_athletes = 2
    for athlete in athletes_models:
        if max_athletes == 0:
            break
        max_athletes -= 1
        parsed_athlete = json.loads(parse_obj_as(AthleteAdmin, athlete).json())
        athletes.append(parsed_athlete)

    equal = verify_athletes(athletes[0], athletes[1])
    print(equal)

    if not equal:
        return

    return

    if athlete is None:
        print("Not Found")
        return
    # private_info = (
    #     db.query(PrivateInfo).filter(PrivateInfo.id == athlete.private_info_id).first()
    # )
    # responsible = (
    #     db.query(Responsible).filter(Responsible.id == athlete.responsible_id).first()
    # )
    # address = db.query(Address).filter(Address.id == athlete.address_id).first()
    # identification_document = (
    #     db.query(IdentificationDocument)
    #     .filter(IdentificationDocument.id == private_info.identification_document_id)
    #     .first()
    # )
    # responsible_identification_document = (
    #     db.query(IdentificationDocument)
    #     .filter(IdentificationDocument.id == responsible.identification_document_id)
    #     .first()
    # )


def merge_atlhetes(class_object1: Any, class_object2: Any):
    for key in class_object1:
        if key == "created_at" or key == "updated_at" or "id" in key:
            continue
        if "dict" in str(type(class_object1[key])):
            merge_atlhetes(class_object1[key], class_object2[key])
            continue
        if "list" in str(type(class_object1[key])):
            if len(class_object1[key]) == 0 or len(class_object2[key]) == 0:
                continue
            if len(class_object1[key]) != len(class_object2[key]):
                print(
                    f"Athletes not equal in {key} {class_object1[key]} vs {class_object2[key]}"
                )
            merge_atlhetes(class_object1[key], class_object2[key])
            continue
        if class_object1[key] is None or class_object2[key] is None:
            continue
        if class_object1[key] != class_object2[key]:
            print(
                f"Athletes not equal in {key} {class_object1[key]} vs {class_object2[key]}"
            )


def verify_athletes(class_object1: Any, class_object2: Any):
    equal = True
    for key in class_object1:
        if key == "created_at" or key == "updated_at" or "id" in key:
            continue
        if "dict" in str(type(class_object1[key])):
            equal = equal and verify_athletes(class_object1[key], class_object2[key])
            continue
        if "list" in str(type(class_object1[key])):
            if len(class_object1[key]) == 0 or len(class_object2[key]) == 0:
                continue
            if len(class_object1[key]) != len(class_object2[key]):
                print(
                    f"Athletes not equal in {key} {class_object1[key]} vs {class_object2[key]}"
                )
            equal = equal and verify_athletes(class_object1[key], class_object2[key])
            continue
        if class_object1[key] is None or class_object2[key] is None:
            continue
        if class_object1[key] != class_object2[key]:
            print(
                f"Athletes not equal in {key} {class_object1[key]} vs {class_object2[key]}"
            )
            equal = False
    return equal


def delete_athlete(athlete_id: UUID4):
    athlete = db.query(Athlete).filter(Athlete.id == athlete_id).first()
    if athlete is None:
        print("Not Found")
        return

    private_info = (
        db.query(PrivateInfo).filter(PrivateInfo.id == athlete.private_info_id).first()
    )
    if private_info is None:
        print("Not Found")
        return
    responsible = (
        db.query(Responsible).filter(Responsible.id == athlete.responsible_id).first()
    )
    if responsible is None:
        print("Not Found")
        return
    address = db.query(Address).filter(Address.id == athlete.address_id).first()
    identification_document = (
        db.query(IdentificationDocument)
        .filter(IdentificationDocument.id == private_info.identification_document_id)
        .first()
    )
    responsible_identification_document = (
        db.query(IdentificationDocument)
        .filter(IdentificationDocument.id == responsible.identification_document_id)
        .first()
    )
    print(athlete.name)
    db.delete(athlete)
    db.delete(private_info)
    db.delete(responsible)
    db.delete(address)
    db.delete(identification_document)
    db.delete(responsible_identification_document)
    db.commit()
    print("DELETED")


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db)
    print("END")
