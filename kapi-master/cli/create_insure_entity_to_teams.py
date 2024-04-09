from models import Team, InsuredEntity
from sql_app import Session
from sqlalchemy import select

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/create_insure_entity_to_teams.py
"""


def main(db: Session):
    team_query = select(Team).distinct()
    print(team_query)
    teams = db.scalars(team_query).all()

    insured_entities = []
    for team in teams:
        insured_entities.append(InsuredEntity(team_id=team.id))
    db.bulk_save_objects(insured_entities)
    db.commit()
    print("Teams done")

    insured_entities_query = select(InsuredEntity).filter(InsuredEntity.team_id != None)
    insured_entities_db = db.scalars(insured_entities_query).all()

    teams_to_update = []
    i = 1
    for insured_entity in insured_entities_db:
        print(f"{i} of {len(insured_entities_db)}")
        i += 1
        for team in teams:
            if team.id == insured_entity.team_id:
                team.insured_entity_id = insured_entity.id
                teams_to_update.append(team)
    db.bulk_save_objects(teams_to_update)
    db.commit()


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
