from datetime import datetime, timedelta
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import and_, or_, text

from core.utils import validate_uuid4
from crud.base import CRUDBase
from models import (
    Athlete,
    AthleteCompetition,
    AthleteGroup,
    Competition,
    Match,
    Team,
    Tournament,
)
from schemas import CompetitionCreate, CompetitionDetails, CompetitionUpdate
from sql_app import Session


class CRUDCompetition(CRUDBase[Competition, CompetitionCreate, CompetitionUpdate]):
    def get(self, db: Session, id: UUID4) -> Competition:
        competition_db = None
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            competition_db = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        if competition_db is None:
            raise HTTPException(404)
        return competition_db

    def get_all_new(
        self,
        db,
        deleted: bool | None,
        show_public: bool | None,
        arquived: bool | None,
        year: int | None,
        inscriptions_open: bool | None,
        competition_ended: bool | None,
        limit: int,
        skip: int,
    ) -> List[CompetitionDetails]:
        today = datetime.now().date()
        # region queries
        where_writted = False

        # Places where or and in the query
        def where_or_and(placed):
            return "and " if placed else "where "

        where_deleted = ""
        if deleted is not None:
            where_deleted = (
                "where c.deleted_at is not null"
                if deleted
                else "where c.deleted_at is null"
            )
            where_writted = True

        where_year = ""
        if year is not None:
            where_year = (
                where_or_and(where_writted)
                + f"date_part('year', c.competition_start) = {year}"
            )

            where_writted = True

        where_show_public = ""
        if show_public is not None:
            where_show_public = (
                where_or_and(where_writted) + f"c.show_public = {show_public}"
            )
            where_writted = True

        # where_arquived = ""
        # if arquived is not None:
        #     where_arquived = where_or_and(where_writted) + f"c.arquived = {arquived}"
        #     where_writted = True

        where_inscriptions_open = ""
        if inscriptions_open is not None:
            where_inscriptions_open = where_or_and(where_writted) + (
                f"c.inscriptions_start <= '{today}' and c.inscriptions_end >= '{today}'"
                if inscriptions_open
                else f"c.inscriptions_start > '{today}' or c.inscriptions_end < '{today}'"
            )
            where_writted = True
        where_competition_ended = ""
        if competition_ended is not None:
            where_competition_ended = where_or_and(where_writted) + (
                f"c.competition_end < '{today}'"
                if competition_ended
                else f"c.competition_end >= '{today}'"
            )

        pagination = f"limit {limit} offset {skip}"

        query_competitions = f"""select c.*, count(distinct t.id) as "tournaments", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
from competitions c
left join tournaments t on t.competition_id = c.id
left join matches m on m.tournament_id = t.id
left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
left join athletes_groups ag on ag.athlete_competition_id = ac.id
left join athletes a on a.id = ag.athlete_id
{where_deleted}
{where_show_public}
{where_inscriptions_open}
{where_competition_ended}
{where_year}
group by c.id
order by c.id
{pagination};"""
        query_direct_winners = f"""select tab1.competition_id as "competition_id", sum(tab1.direct_winners) as "direct_winers"
from (select c.id as "competition_id", c.name as "competition_name", t.id, sum(case when m.athlete_blue_id is null and m.athlete_red_id is not null then 1 else 0 end) as "direct_winners"
from competitions c 
left join tournaments t on t.competition_id = c.id 
left join matches m on m.tournament_id = t.id
{where_deleted}
{where_show_public}
{where_inscriptions_open}
{where_competition_ended}
{where_year}
group by t.id, c.id
having count(t.id) = 1) as tab1
group by tab1.competition_id
order by tab1.competition_id
{pagination};"""
        # endregion
        competitions = db.execute(text(query_competitions)).all()
        direct_winners = db.execute(text(query_direct_winners)).all()
        results: List[CompetitionDetails] = []
        for competition in competitions:
            result = competition._asdict() | {"direct_winners": 0}
            for direct_winner in direct_winners:
                if direct_winner.competition_id == competition.id:
                    result["direct_winners"] = direct_winner[1]
                    break
            results.append(result)
        return results

    def get_name(self, db: Session, id: UUID4) -> str:
        competition_db = None
        if not validate_uuid4(id):
            raise HTTPException(404)
        try:
            competition_db = db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        if competition_db is None:
            raise HTTPException(404)
        return str(competition_db.name)

    def get_by_name(self, db: Session, name: str) -> Optional[Competition]:
        try:
            return db.query(self.model).filter(self.model.name == name).first()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def get_all(self, db: Session) -> List[Competition]:
        try:
            return db.query(self.model).filter(self.model.deleted_at is None).all()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def get_tournaments_of_athlete(
        self, db: Session, competition_id: str, athlete_id: str
    ):
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        if not validate_uuid4(athlete_id):
            raise HTTPException(404)
        try:
            return (
                db.query(Tournament)
                .join(Match)
                .join(
                    AthleteCompetition,
                    or_(
                        Match.athlete_blue_id == AthleteCompetition.id,
                        Match.athlete_red_id == AthleteCompetition.id,
                    ),
                )
                .join(
                    AthleteGroup,
                    AthleteGroup.athlete_competition_id == AthleteCompetition.id,
                )
                .join(Athlete, Athlete.id == AthleteGroup.athlete_id)
                .filter(
                    and_(
                        Tournament.competition_id == competition_id,
                        Athlete.id == athlete_id,
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def get_tournaments_of_team(self, db: Session, competition_id: str, team_id: str):
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        if not validate_uuid4(team_id):
            raise HTTPException(404)
        try:
            return (
                db.query(Tournament)
                .join(Match)
                .join(
                    AthleteCompetition,
                    or_(
                        Match.athlete_blue_id == AthleteCompetition.id,
                        Match.athlete_red_id == AthleteCompetition.id,
                    ),
                )
                .join(
                    AthleteGroup,
                    AthleteGroup.athlete_competition_id == AthleteCompetition.id,
                )
                .join(Athlete, Athlete.id == AthleteGroup.athlete_id)
                .join(Team, Team.id == Athlete.team_id)
                .filter(
                    and_(
                        Tournament.competition_id == competition_id, Team.id == team_id
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def get_athletes_competition(
        self,
        db: Session,
        competition_id: str,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        day: Optional[int] = None,
        time: Optional[bool] = None,
        gender: Optional[bool] = None,
        adapted: Optional[bool] = None,
    ):
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        query = (
            db.query(Athlete)
            .join(AthleteGroup)
            .join(AthleteCompetition)
            .join(
                Match,
                or_(
                    Match.athlete_red_id == AthleteCompetition.id,
                    Match.athlete_blue_id == AthleteCompetition.id,
                ),
            )
            .join(Tournament)
            .filter(AthleteCompetition.competition_id == competition_id)
        )

        if age_min is not None:
            query = query.filter(
                Athlete.birthday <= datetime.today() - relativedelta(years=age_min)
            )
        if age_max is not None:
            query = query.filter(
                Athlete.birthday >= datetime.today() - relativedelta(years=age_max)
            )
        if day is not None:
            query = query.filter(Tournament.day == day)
        if time is not None:
            query = query.filter(Tournament.morning == time)
        if gender is not None:
            query = query.filter(Athlete.is_male == gender)
        if adapted is not None:
            query = query.filter(Athlete.is_adapted == time)

        return query.distinct().count()

    def get_results(self, db: Session, competition_ids: list[str]):
        for id in competition_ids:
            if not validate_uuid4(id):
                raise HTTPException(404)

            competition_ids_where = ""
            if len(competition_ids) == 1:
                competition_ids_where = (
                    f"""and t.competition_id = '{competition_ids[0]}'"""
                )
            else:
                first = True
                for id in competition_ids:
                    if first:
                        competition_ids_where = f"""and (t.competition_id = '{id}'"""
                    first = False
                    competition_ids_where += f"""or t.competition_id = '{id}'"""
                competition_ids_where += ")"

        return_data = {
            "first": [],
            "second": [],
            "third": [],
            "direct": [],
        }

        direct_winners = db.execute(
            text(
                f"""select t2.tournament_id
from matches m2
join (select m.tournament_id
from matches m
join tournaments t on m.tournament_id = t.id
where t.first_place_id is not null
	{competition_ids_where}
group by m.tournament_id
having count(m.tournament_id) = 1) as t2 on m2.tournament_id = t2.tournament_id
    where m2.athlete_red_id is not null
    and m2.athlete_blue_id is null"""
            )
        )

        # region sql queries for combats

        db_data = {
            "first": [],
            "second": [],
            "third": [],
        }

        sql_string = (
            """select sum(case when m.athlete_red_id is not null and m.athlete_blue_id is not null and (m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id) and m.winner_id = t.{place}_place_id then 1 else 0 end) as matches_participated_count, count(m.id) as matches_count, ac.id as "athlete_competition_id", a.id as "athlete_id", t.id as "tournament_id", a.name as "athlete_name", a.birthday as "athlete_birthday", t2.name as "team_name", t2.abbreviation as "team_abbreviation", t2.id as "team_id", c.name as "category_name", co.calculate_age_start_year as "calculate_age_start_year", ct.name as "category_type_name", co.competition_start as "competition_start_date", t.competition_id as "competition_id"
from tournaments t 
join matches m on m.tournament_id = t.id
join categories c on c.id = t.category_id 
join category_types ct on ct.id = c.category_type_id 
join athlete_competitions ac on ac.id = t.{place}_place_id 
join athletes_groups ag on ag.athlete_competition_id = ac.id
join athletes a on ag.athlete_id = a.id
join teams t2 on t2.id = a.team_id 
join competitions co on t.competition_id = co.id
where t.first_place_id is not null
    """
            + f"{competition_ids_where}"
            + """
group by ac.id, a.id, t.id, a.name, a.birthday,  t2.name, t2.abbreviation, t2.id, c.name, co.calculate_age_start_year, ct.name, co.competition_start
order by t.id;"""
        )

        db_data["first"] = db.execute(text(sql_string.format(place="first")))
        db_data["second"] = db.execute(text(sql_string.format(place="second")))
        db_data["third"] = db.execute(text(sql_string.format(place="third")))
        # endregion

        for place in direct_winners:
            return_data["direct"].append({"tournament_id": place.tournament_id})

        for place in ["first", "second", "third"]:
            for result in db_data[place]:
                return_data[place].append(
                    {
                        "athlete_competition_id": result.athlete_competition_id,
                        "athlete_id": result.athlete_id,
                        "tournament_id": result.tournament_id,
                        "competition_id": result.competition_id,
                        "athlete_name": result.athlete_name,
                        "athlete_birthday": result.athlete_birthday,
                        "team_id": result.team_id,
                        "team_name": result.team_name,
                        "team_abbreviation": result.team_abbreviation,
                        "category_name": result.category_name,
                        "matches_count": result.matches_count,
                        "matches_participated_count": result.matches_participated_count,
                        "category_type_name": result.category_type_name,
                        "competition_start_date": result.competition_start_date,
                    }
                )

        return return_data

    def get_matches_each_area(self, db: Session, competition_id: str):
        if not validate_uuid4(competition_id):
            raise HTTPException(404)
        return (
            db.query(Match)
            .join(Tournament)
            .filter(
                Tournament.competition_id == competition_id,
                Match.winner_id == None,
                Match.call_type != None,
            )
            .all()
        )

    def get_all_filtered(self, db: Session, is_admin: bool, is_anon: bool):
        if is_admin:
            sql_string_admin = """select c.*, count(distinct t.id) as "tournaments", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
            from competitions c
            left join tournaments t on t.competition_id = c.id
            left join matches m on m.tournament_id = t.id
            left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
            left join athletes_groups ag on ag.athlete_competition_id = ac.id
            left join athletes a on a.id = ag.athlete_id
            where c.deleted_at is null
            group by c.id"""

            sql_string_direct_winners = """select tab1.competition_id as "competition_id", sum(tab1.direct_winners) as "direct_winners"
            from (select c.id as "competition_id", c.name as "competition_name", t.id, sum(case when m.athlete_blue_id is null and m.athlete_red_id is not null then 1 else 0 end) as "direct_winners"
            from competitions c 
            left join tournaments t on t.competition_id = c.id 
            left join matches m on m.tournament_id = t.id
            group by t.id, c.id
            having count(t.id) = 1) as tab1
            group by tab1.competition_id"""
            try:
                query_results = db.execute(text(sql_string_admin))
                query_winners_results = db.execute(text(sql_string_direct_winners))
                competition_json = []

                for result in query_results:
                    no_winners = True
                    for winners in query_winners_results:
                        if str(winners.competition_id) == str(result.id):
                            no_winners = False
                            competition_json.append(
                                {
                                    "name": result.name,
                                    "id": str(result.id),
                                    "tournaments": result.tournaments,
                                    "matches": result.matches,
                                    "direct_winners": int(winners.direct_winners),
                                    "athletes": result.athletes,
                                    "competition_start": result.competition_start,
                                }
                            )
                            break
                    if no_winners:
                        competition_json.append(
                            {
                                "name": result.name,
                                "id": str(result.id),
                                "tournaments": result.tournaments,
                                "matches": result.matches,
                                "direct_winners": 0,
                                "athletes": result.athletes,
                                "competition_start": result.competition_start,
                            }
                        )
                return competition_json
            except Exception as e:
                print(e)
                db.rollback()
                raise HTTPException(status_code=503, detail="DB Error")
        else:
            query_string = ""
            if is_anon:
                query_string = f"""select c.id as "id", c.name as "name", c.competition_start as "competition_start", c.competition_end as "competition_end", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
                from competitions c
                left join tournaments t on t.competition_id = c.id
                left join matches m on m.tournament_id = t.id
                left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
                left join athletes_groups ag on ag.athlete_competition_id = ac.id
                left join athletes a on a.id = ag.athlete_id
                where c.deleted_at is null
                    and c.show_public = true
                    and c.competition_start < '{datetime.today()}'
                group by c.id"""
            else:
                query_string = """select c.id as "id", c.name as "name", c.competition_start as "competition_start", c.competition_end as "competition_end", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
                from competitions c
                left join tournaments t on t.competition_id = c.id
                left join matches m on m.tournament_id = t.id
                left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
                left join athletes_groups ag on ag.athlete_competition_id = ac.id
                left join athletes a on a.id = ag.athlete_id
                where c.deleted_at is null
                    and c.show_public = true
                group by c.id"""
            try:
                query_results = db.execute(text(query_string))
                competition_json = []
                for result in query_results:
                    competition_json.append(
                        {
                            "name": result.name,
                            "id": str(result.id),
                            "matches": result.matches,
                            "athletes": result.athletes,
                            "competition_start": result.competition_start,
                            "competition_end": result.competition_end,
                        }
                    )
                return competition_json
            except Exception as e:
                print(e)
                db.rollback()
                raise HTTPException(status_code=503, detail="DB Error")

    def get_past(self, db: Session):
        query_string = f"""select c.id as "id", c.name as "name", c.competition_start as "competition_start", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
        from competitions c
        left join tournaments t on t.competition_id = c.id
        left join matches m on m.tournament_id = t.id
        left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
        left join athletes_groups ag on ag.athlete_competition_id = ac.id
        left join athletes a on a.id = ag.athlete_id
        where c.deleted_at is null
            and c.show_public = true
            and c.competition_end < '{datetime.today() - timedelta(days=1)}'
        group by c.id"""
        try:
            query_results = db.execute(text(query_string))
            competition_json = []
            for result in query_results:
                competition_json.append(
                    {
                        "name": result.name,
                        "id": str(result.id),
                        "matches": result.matches,
                        "athletes": result.athletes,
                        "competition_start": result.competition_start,
                    }
                )
            return competition_json
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def get_inscriptions(self, db: Session) -> List[Competition]:
        today = datetime.now()
        try:
            return (
                db.query(Competition)
                .filter(
                    and_(
                        Competition.deleted_at is None,
                        and_(
                            Competition.inscriptions_start < today,
                            Competition.inscriptions_end > today,
                        ),
                    )
                )
                .all()
            )
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")

    def create(self, db: Session, db_obj: Competition) -> Competition:
        db.add(db_obj)
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        db.refresh(db_obj)
        return db_obj

    def update_show(
        self, db: Session, db_obj: Competition, obj_in: Competition
    ) -> Optional[Competition]:
        db_obj.show_public = obj_in.show_public
        db.add(db_obj)
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        db.refresh(db_obj)
        return db_obj

    def update_notes(
        self, db: Session, db_obj: Competition, notes: str
    ) -> Optional[Competition]:
        db_obj.notes = notes
        db.add(db_obj)
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: Competition, obj_in: Competition
    ) -> Optional[Competition]:
        db_obj.name = obj_in.name if obj_in.name is not None else db_obj.name
        db_obj.inscriptions_start = (
            obj_in.inscriptions_start
            if obj_in.inscriptions_start is not None
            else db_obj.inscriptions_start
        )
        db_obj.inscriptions_end = (
            obj_in.inscriptions_end
            if obj_in.inscriptions_end is not None
            else db_obj.inscriptions_end
        )
        db_obj.competition_start = (
            obj_in.competition_start
            if obj_in.competition_start is not None
            else db_obj.competition_start
        )
        db_obj.competition_end = (
            obj_in.competition_end
            if obj_in.competition_end is not None
            else db_obj.competition_end
        )
        db_obj.calculate_age_start_year = (
            obj_in.calculate_age_start_year
            if obj_in.calculate_age_start_year is not None
            else db_obj.calculate_age_start_year
        )
        db_obj.notes = obj_in.notes if obj_in.notes is not None else db_obj.notes
        db.add(db_obj)
        try:
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=503, detail="DB Error")
        db.refresh(db_obj)
        return db_obj


competition = CRUDCompetition(Competition)
