from models import Athlete, PrivateInfo
from sql_app import Session
from sqlalchemy import select

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/find_duplicate_athletes.py
"""
MAX_FED_NUM = 12000
FED_NUM_START = 9950
MATCHES_TO_PASS = 1


def main(db: Session):
    passed = 0
    for fed_num in range(FED_NUM_START, MAX_FED_NUM):
        print(f"Querying for {fed_num}")
        athlete_query = (
            select(Athlete)
            .join(PrivateInfo)
            .filter(PrivateInfo.federation_number == fed_num)
        )

        athletes = db.scalars(athlete_query).all()
        if len(athletes) < 2:
            continue

        if passed < MATCHES_TO_PASS:
            passed += 1
            continue

        print(f"Fed_num: {fed_num}")
        for athlete in athletes:
            print(
                f"name: {athlete.name}, id: {athlete.id}, private: {athlete.private_info_id}, birthday: {athlete.birthday}"
            )
        break


if __name__ == "__main__":
    db: Session = Session()
    main(db=db)
    print("END")
