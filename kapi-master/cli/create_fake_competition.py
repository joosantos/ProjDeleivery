import traceback
import datetime
from random import shuffle
from core.utils import get_password_hash
from models import (
    Category,
    AthleteGroup,
    AthleteCompetition,
    User,
    Team,
    Competition,
    Tournament,
    PrivateInfo,
    Address,
    IdentificationDocument,
    Belt,
    Responsible,
    Inscription,
    Athlete,
    UserRole,
    Role,
)
from kapi.cli.init_db import populate_db
from core.tournaments_utils import (
    resolve_matches_of_tournament,
    create_matches_for_tournament,
    number_matches_area,
)

from core.utils import commit_to_bd
from sql_app import Session

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/create_fake_competition.py
"""


def main(db: Session):
    populate_db(db=db)
    format = "%d-%m-%Y"
    athletes = [
        "Miguel",
        "João",
        "Pedro",
        "Mário",
        "Ricardo",
        "Afonso",
        "José",
        "Rui",
        "Tiago",
        "Manuel",
        "Carlos",
        "Luís",
        "Rafael",
        "Daniel",
        "Joaquim",
        "André",
    ]
    athletes_competition = []
    tournaments = []
    tournaments_inscriptions = []
    white_belt = get_from_bd_first(db.query(Belt).filter(Belt.name == "white"))
    if white_belt is None:
        raise Exception("No White Belt")
    print("Creating Coach")
    coach_identification_document = IdentificationDocument()
    db.add(coach_identification_document)
    coach_identification_document = commit_to_bd(
        session_db=db, db_obj=coach_identification_document
    )
    if coach_identification_document is None:
        raise Exception("No Coach Identification Document")
    coach_private_info = PrivateInfo(
        identification_document_id=coach_identification_document.id
    )
    db.add(coach_private_info)
    coach_private_info = commit_to_bd(session_db=db, db_obj=coach_private_info)
    if coach_private_info is None:
        raise Exception("No Coach Private Info")
    coach_identification_document = IdentificationDocument()
    db.add(coach_identification_document)
    coach_identification_document = commit_to_bd(
        session_db=db, db_obj=coach_identification_document
    )
    coach_address = Address()
    db.add(coach_address)
    coach_address = commit_to_bd(session_db=db, db_obj=coach_address)
    if coach_address is None:
        raise Exception("No Coach Address")
    coach = User(
        name="Fake Coach",
        hashed_password=get_password_hash("123"),
        email="fake@email.pt",
        email_verified=True,
        admin_verified=True,
        is_active=True,
        private_info_id=coach_private_info.id,
        address_id=coach_address.id,
    )
    db.add(coach)
    coach = commit_to_bd(
        session_db=db,
        db_obj=coach,
    )
    if coach is None:
        raise Exception("No Coach")
    role = get_from_bd_first(db.query(Role).filter(Role.name == "COACH"))
    if role is None:
        raise Exception("No Role")
    coach_role = UserRole(user_id=coach.id, role_id=role.id)
    db.add(coach_role)
    commit_to_bd(session_db=db, db_obj=coach_role)
    print("Creating Team")
    team = Team(
        name="Fake Team",
        abbreviation="FT",
        association="Fake Association",
        coach_id=coach.id,
    )
    db.add(team)
    team = commit_to_bd(
        session_db=db,
        db_obj=team,
    )
    if team is None:
        raise Exception("No Team")
    print("Creating Competition")
    competition = Competition(
        name="Fake Competition",
        show_public=True,
        calculate_age_start_year=True,
        notes="",
        inscriptions_start=datetime.datetime.strptime("25-01-2023", format),
        inscriptions_end=datetime.datetime.strptime("26-01-2023", format),
        competition_start=datetime.datetime.strptime("27-01-2023", format),
        competition_end=datetime.datetime.strptime("26-03-2023", format),
    )
    db.add(competition)
    competiton = commit_to_bd(
        session_db=db,
        db_obj=competition,
    )
    if competiton is None:
        raise Exception("No Competition")
    categories = (
        db.query(Category)
        .filter(
            Category.name.in_(
                ["Rumble Kids", "Light Kempo", "Formas c/ Armas", "Formas Mão Vazia"]
            )
        )
        .all()
    )

    i = 0
    morning = True
    print("Creating Tournaments")
    for category in categories:
        print(f"Creating Tournament of Category {category.name}")
        if i == 4:
            morning = False
        for weight in [50, 60]:
            i += 1
            tournament_in = Tournament(
                competition_id=competiton.id,
                category_id=category.id,
                is_male=True,
                age_min=5 * i,
                age_max=4 + 5 * i,
                day=1,
                order=i if morning else i - 4,
                morning=morning,
                weight_min=weight,
                weight_max=weight + 5,
                area=1,
            )
            db.add(tournament_in)
            tournaments.append(commit_to_bd(session_db=db, db_obj=tournament_in))

    print("Creating Athletes")
    for athlete in athletes:
        print(f"Creating Athelte {athlete}")
        athlete_identification = IdentificationDocument()
        db.add(athlete_identification)
        athlete_identification = commit_to_bd(
            session_db=db, db_obj=athlete_identification
        )
        if athlete_identification is None:
            raise Exception("No Athlete Identification")
        athlete_private_info = PrivateInfo(
            identification_document_id=athlete_identification.id
        )
        db.add(athlete_private_info)
        athlete_private_info = commit_to_bd(
            session_db=db,
            db_obj=athlete_private_info,
        )
        if athlete_private_info is None:
            raise Exception("No Athlete Private Info")
        athlete_address = Address()
        db.add(athlete_address)
        athlete_address = commit_to_bd(session_db=db, db_obj=athlete_address)
        if athlete_address is None:
            raise Exception("No Athlete Address")
        responsible_identification = IdentificationDocument()
        db.add(responsible_identification)
        responsible_identification = commit_to_bd(
            session_db=db, db_obj=responsible_identification
        )
        if responsible_identification is None:
            raise Exception("No Responsible Indetification")
        athlete_responsible = Responsible(
            identification_document_id=responsible_identification.id
        )
        db.add(athlete_responsible)
        athlete_responsible = commit_to_bd(session_db=db, db_obj=athlete_responsible)
        if athlete_responsible is None:
            raise Exception("No Athlete Responsible")
        athlete_db = Athlete(
            name=athlete,
            birthday=datetime.datetime.strptime("01-01-2000", format),
            weight=60,
            is_male=True,
            is_adapted=False,
            team_id=team.id,
            belt_id=white_belt.id,
            private_info_id=athlete_private_info.id,
            address_id=athlete_address.id,
            responsible_id=athlete_responsible.id,
        )
        db.add(athlete_db)
        athlete_db = commit_to_bd(session_db=db, db_obj=athlete_db)
        if athlete_db is None:
            raise Exception("No Athlete")
        athlete_competition = AthleteCompetition(competition_id=competiton.id)
        db.add(athlete_competition)
        athlete_competition = commit_to_bd(session_db=db, db_obj=athlete_competition)
        if athlete_competition is None:
            raise Exception("No Athlete Competition")
        athletes_competition.append(athlete_competition)
        athlete_group = AthleteGroup(
            athlete_id=athlete_db.id, athlete_competition_id=athlete_competition.id
        )

        db.add(athlete_group)
        commit_to_bd(session_db=db, db_obj=athlete_group)

    i = 0
    print("Creating Inscriptions")
    for tournament in tournaments:
        print(
            f"Creating Inscriptions for tournament {tournament.category.name} - {tournament.weight_min} / {tournament.weight_max} Kg."
        )
        i += 1
        if i % 6 == 0:
            i += 1
        j = 0
        for athlete_competition_db in athletes_competition:
            if ((i % 6) + 1) * 3 - ((i + 1) % 2) == j:
                break
            inscription = Inscription(
                tournament_id=tournament.id,
                athlete_competition_id=athlete_competition_db.id,
                confirmed=True,
                accepted=True,
            )
            db.add(inscription)
            commit_to_bd(session_db=db, db_obj=inscription)
            j += 1
    print("Getting Tournaments with the inscriptions")
    tournaments_inscriptions = (
        db.query(Tournament).filter(Tournament.competition_id == competiton.id).all()
    )

    print("Creating the Matches")
    for tournament in tournaments_inscriptions:
        print(
            f"Creating Matches for tournament {tournament.category.name} - {tournament.weight_min} / {tournament.weight_max} Kg."
        )
        if len(tournament.inscriptions) == 0:
            print("No Matches To Create")
            continue
        shuffle(tournament.inscriptions)
        inscriptions_ids = []
        for inscription in tournament.inscriptions:
            if inscription.accepted and inscription.confirmed:
                inscriptions_ids.append(inscription.athlete_competition_id)
        create_matches_for_tournament(
            db=db,
            tournament=tournament,
        )
        resolve_matches_of_tournament(db=db, tournament=tournament, athlete_bye_id=None)
    print("Numering Matches")
    number_matches_area(
        db=db, tournaments_array=tournaments_inscriptions, athlete_bye_id=None
    )


def get_from_bd_first(sql_string):
    try:
        return sql_string.first()
    except Exception as e:
        handleException(e)


def handleException(e):
    print(e)
    db.rollback()
    traceback.print_exc(e)
    raise Exception("Exception Occurred")


if __name__ == "__main__":
    gen = get_db()
    db: Session = next(gen)
    main(db=db)
    print("END")
