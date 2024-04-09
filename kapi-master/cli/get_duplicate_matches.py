from sql_app.database import db
from datetime import datetime
from typing import List, Optional
from sqlalchemy import and_
from models import Match


def read():
    matches = db.query(Match).all()

    with open("../matches.txt", "w") as file:
        for match in matches:
            if match.tournament_id is not None:
                file.write(f"{match.id},{match.tournament_id}\n")


def write():
    with open("../matches.txt", "r") as file:
        lines = file.readlines()
        count = len(lines)
        counter = 1
        for line in lines:
            print(f"line {counter} of {count}")
            counter += 1
            ids = line.replace("\n", "").split(",")
            match_db = db.query(Match).filter(Match.id == ids[0]).first()
            if match_db is not None and match_db.tournament_id is None:
                match_db.tournament_id = ids[1]
                db.add(match_db)
                try:
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                    raise Exception("Error writing to DB")


if __name__ == "__main__":
    write()
    # read()
    print("END")
