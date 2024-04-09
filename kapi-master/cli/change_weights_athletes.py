from models import Competition, Tournament, Inscription
import crud
from sql_app import Session
from sqlalchemy import select
import pandas as pd
from core.utils import commit_to_bd

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/change_weights_athletes.py
"""

OUTPUT_FILE = "cli/output_links.txt"

COMPETITION_ID = "eccb9b9b-4387-4789-ba7e-677af3e40b1e"

output = {}


def main(db: Session):
    competition: Competition = crud.competition.get(db=db, id=COMPETITION_ID)
    total_tournaments = len(competition.tournaments)
    i = 0
    for tournament in competition.tournaments:
        i = i + 1
        print(f"Tournament {i} of {total_tournaments}")
        if tournament.weight_min is None and tournament.weight_max is None:
            continue
        if len(tournament.inscriptions) == 0:
            continue
        min = tournament.weight_min
        max = tournament.weight_max
        if min is None:
            min = max - 5
        if max is None:
            max = 999
        for inscription in tournament.inscriptions:
            athlete = inscription.athlete_competition.athletes_group[0].athlete
            if athlete.weight > max or athlete.weight < min:
                index_team = f"{athlete.team.name}.{athlete.team.abbreviation}"
                if index_team not in output:
                    output[index_team] = []
                output[index_team].append(
                    {
                        "name": athlete.name,
                        "category": tournament.category.name,
                        "link": f"https://kempo-frontend.herokuapp.com/inscription/edit/{tournament.id}/{inscription.athlete_competition_id}",
                    }
                )

    with open(OUTPUT_FILE, "w") as output_file:
        for team in output:
            # team_name = team.split(".")[0]
            # team_abbreviation = team.split(".")[1]
            # output_file.write(f"TEAM {team_name} ({team_abbreviation})\n")
            for athlete in output[team]:
                # output_file.write(
                #     f"\tAthlete {athlete['name']}, in {athlete['category']}, link: {athlete['link']}\n"
                # )
                output_file.write(f"{athlete['link']}\n")
            # output_file.write("\n\n")

    return


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
