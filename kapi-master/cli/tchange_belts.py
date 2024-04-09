from sql_app.database import db
from datetime import datetime
from typing import List, Optional
from sqlalchemy import and_, select, func, text, or_, Integer
from schemas import AthleteCreate, TournamentCreate, TournamentUpdate, InscriptionCreate
from core.environment import config
import asyncio
from core.utils import get_password_hash
import crud


def update_belts(tournament_obj):
    db.add(tournament_obj)
    try:
        db.commit()
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=503, detail="Error writing to DB")
    db.refresh(tournament_obj)
    return tournament_obj


competition_id = "e6396c34-b6a2-4d10-984f-54bf46a0f148"

competition = crud.competition.get(id=competition_id)

white_belt = crud.belt.get_by_name("white")
orange_belt = crud.belt.get_by_name("orange")
orange_purple_belt = crud.belt.get_by_name("orange-purple")
purple_belt = crud.belt.get_by_name("purple")
green_belt = crud.belt.get_by_name("green")
brown_belt = crud.belt.get_by_name("brown")
black_belt = crud.belt.get_by_name("black")

categories_forms = [
    "Formas Mão Vazia Hard",
    "Formas Mão Vazia Soft",
    "Formas com Armas Hard",
    "Formas com Armas Soft",
]
count = 0
number_tournaments = len(competition.tournaments)
for tournament in competition.tournaments:
    count += 1
    print(f"Processing Tournament number {count} of {number_tournaments}")
    tournament_id = tournament.id
    if tournament.belt_min_id is not None:
        continue
    if tournament.category.name in categories_forms:
        inscriptions = tournament.inscriptions
        tournament_white = crud.tournament.create(
            obj_in=TournamentCreate(
                category_id=tournament.category_id,
                competition_id=competition_id,
                age_min=tournament.age_min,
                age_max=tournament.age_max,
                is_male=tournament.is_male,
                belt_min_id=white_belt.id,
                belt_max_id=orange_belt.id,
            )
        )
        tournament_purple = crud.tournament.create(
            obj_in=TournamentCreate(
                category_id=tournament.category_id,
                competition_id=competition_id,
                age_min=tournament.age_min,
                age_max=tournament.age_max,
                is_male=tournament.is_male,
                belt_min_id=purple_belt.id,
                belt_max_id=green_belt.id,
            )
        )
        tournament.belt_min_id = brown_belt.id
        tournament.belt_max_id = black_belt.id
        tournament_brown = update_belts(tournament_obj=tournament)
        for inscription in inscriptions:
            highest_belt_order = 0
            for athlete in inscription.athlete_competition.athletes_group:
                if athlete.athlete.belt.order > highest_belt_order:
                    highest_belt_order = athlete.athlete.belt.order
            if highest_belt_order <= orange_purple_belt.order:
                crud.inscription.create(
                    InscriptionCreate(
                        tournament_id=tournament_white.id,
                        athlete_competition_id=inscription.athlete_competition_id,
                        confirmed=True,
                    )
                )
                crud.inscription.delete_inscription(
                    tournament_id=tournament_id,
                    athlete_competition_id=inscription.athlete_competition_id,
                )
            elif highest_belt_order <= green_belt.order:
                crud.inscription.create(
                    InscriptionCreate(
                        tournament_id=tournament_purple.id,
                        athlete_competition_id=inscription.athlete_competition_id,
                        confirmed=True,
                    )
                )
                crud.inscription.delete_inscription(
                    tournament_id=tournament_id,
                    athlete_competition_id=inscription.athlete_competition_id,
                )

    elif tournament.category.name == "Semi Kempo":
        inscriptions = tournament.inscriptions
        tournament_white = crud.tournament.create(
            obj_in=TournamentCreate(
                category_id=tournament.category_id,
                competition_id=competition_id,
                age_min=tournament.age_min,
                age_max=tournament.age_max,
                weight_min=tournament.weight_min,
                weight_max=tournament.weight_max,
                is_male=tournament.is_male,
                belt_min_id=white_belt.id,
                belt_max_id=orange_belt.id,
            )
        )

        tournament.belt_min_id = purple_belt.id
        tournament.belt_max_id = black_belt.id
        tournament_purple = update_belts(tournament_obj=tournament)
        for inscription in inscriptions:
            highest_belt_order = 0
            for athlete in inscription.athlete_competition.athletes_group:
                if athlete.athlete.belt.order > highest_belt_order:
                    highest_belt_order = athlete.athlete.belt.order
            if highest_belt_order <= orange_purple_belt.order:
                crud.inscription.create(
                    InscriptionCreate(
                        tournament_id=tournament_white.id,
                        athlete_competition_id=inscription.athlete_competition_id,
                        confirmed=True,
                    )
                )
                crud.inscription.delete_inscription(
                    tournament_id=tournament_id,
                    athlete_competition_id=inscription.athlete_competition_id,
                )
