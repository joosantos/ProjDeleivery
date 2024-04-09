from models import (
    Athlete,
    PrivateInfo,
    Team,
    IdentificationDocument,
    Responsible,
    Address,
    InsuredEntity,
)
from sql_app import Session
from sqlalchemy import select
import csv
from datetime import datetime
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/import_athletes.py
"""

MAX_FED_NUMBER = 10904
FED_NUM = "Nº Fed"
NAME = "Nome"
TEAM_ABR = "Abreviatura"
BIRTHDAY = "D. Nascimento"
CC = "C. Cidadão"
NIF = "NIF"
GENDER = "Gênero"
ADDRESS = "Morada "
ZIP_CODE = "Código Postal"
CITY = "Localidade"
DISTRICT = "Distrito"
REGION = "Região"
EMAIL = "Email"
PHONE = "Telemóvel"
SKIP_FIRST = 0


def main(db: Session):
    with open("./cli/fplk_db.csv") as csv_file:
        spamreader = csv.DictReader(csv_file)
        teams_cache = {}
        plus_started = True
        for row in spamreader:
            print(row[FED_NUM])
            if not plus_started:
                plus_started = "+" in row[FED_NUM]
            fed_num = int(row[FED_NUM].replace("*", "").replace("+", "").strip())
            # Skipper
            if fed_num < SKIP_FIRST:
                continue

            athlete_query = (
                select(Athlete)
                .join(PrivateInfo)
                .filter(PrivateInfo.federation_number == fed_num)
            )
            athletes: list[Athlete] = db.scalars(athlete_query).all()
            if len(athletes) == 0 or (plus_started and "+" in row[FED_NUM]):
                team_id = None
                name = row[NAME].strip() or None
                birthday = row[BIRTHDAY].strip() or None
                team_abr = row[TEAM_ABR].strip() or None
                cc = row[CC].strip() or None
                nif = row[NIF].strip() or None
                gender = row[GENDER].strip().upper() or None
                address = row[ADDRESS].strip() or None
                zip_code = row[ZIP_CODE].strip() or None
                city = row[CITY].strip() or None
                district = row[DISTRICT].strip() or None
                region = row[REGION].strip() or None
                email = row[EMAIL].strip() or None
                phone = row[PHONE].strip() or None
                if name is None:
                    continue
                if birthday is not None:
                    if "-" in birthday:
                        numbers = birthday.split("-")
                        if int(numbers[0]) > 12:
                            birthday = datetime.strptime(birthday, "%d-%m-%Y")
                        else:
                            birthday = datetime.strptime(birthday, "%m-%d-%Y")
                    else:
                        numbers = birthday.split("/")
                        if int(numbers[0]) > 1000:
                            birthday = datetime.strptime(birthday, "%Y/%m/%d")
                        elif int(numbers[1]) > 12:
                            birthday = datetime.strptime(birthday, "%m/%d/%Y")
                        else:
                            birthday = datetime.strptime(birthday, "%d/%m/%Y")
                if team_abr is not None:
                    if team_abr not in teams_cache:
                        team_query = select(Team).filter(Team.abbreviation == team_abr)
                        team: Team = db.scalars(team_query).first()
                        if team is None:
                            teams_cache[team_abr] = None
                        else:
                            teams_cache[team_abr] = team.id
                    team_id = teams_cache[team_abr]
                if gender != "F" or gender != "M":
                    gender = None
                create_athlete(
                    db=db,
                    name=name,
                    birthday=birthday,
                    cc=cc,
                    nif=nif,
                    gender=gender,
                    address=address,
                    zip_code=zip_code,
                    city=city,
                    district=district,
                    region=region,
                    email=email,
                    phone=phone,
                    fed_num=fed_num,
                    team_id=team_id,
                )

        return


def create_athlete(
    db: Session,
    name,
    birthday,
    cc,
    nif,
    gender,
    address,
    zip_code,
    city,
    district,
    region,
    email,
    phone,
    fed_num,
    team_id,
):
    responsible_identification_document = IdentificationDocument()
    if cc is not None:
        responsible_identification_document = IdentificationDocument(
            type="C", number=cc
        )
    db.add(responsible_identification_document)
    responsible_identification_document = commit_to_bd(
        session_db=db, db_obj=responsible_identification_document
    )
    responsible = Responsible(
        identification_document_id=responsible_identification_document.id
    )
    db.add(responsible)
    responsible = commit_to_bd(session_db=db, db_obj=responsible)
    address = Address(
        address=address, zip_code=zip_code, city=city, district=district, region=region
    )
    db.add(address)
    address = commit_to_bd(session_db=db, db_obj=address)
    identification_document = IdentificationDocument()
    db.add(identification_document)
    identification_document = commit_to_bd(
        session_db=db, db_obj=identification_document
    )
    private_info = PrivateInfo(
        identification_document_id=identification_document.id,
        federation_number=fed_num,
        email=email,
        nif=nif,
        gender_is_male=gender,
        phone_number=phone,
    )
    db.add(private_info)
    private_info = commit_to_bd(session_db=db, db_obj=private_info)
    athlete = Athlete(
        name=name,
        responsible_id=responsible.id,
        private_info_id=private_info.id,
        address_id=address.id,
        is_male=gender == "M",
        birthday=birthday,
        team_id=team_id,
    )
    db.add(athlete)
    athlete = commit_to_bd(session_db=db, db_obj=athlete)

    insured_entity = InsuredEntity(athlete_id=athlete.id)
    db.add(insured_entity)
    insured_entity = commit_to_bd(session_db=db, db_obj=insured_entity)

    athlete.insured_entity_id = insured_entity.id
    db.add(athlete)
    athlete = commit_to_bd(session_db=db, db_obj=athlete)


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
