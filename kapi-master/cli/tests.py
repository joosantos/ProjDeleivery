from sql_app.database import db
from sqlalchemy import text
import json
from models import Competition
from datetime import datetime, timedelta

sql_string_admin = """select c.id as "id", c.name as "name", count(distinct t.id) as "tournaments", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
from competitions c
left join tournaments t on t.competition_id = c.id
left join matches m on m.tournament_id = t.id
left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
left join athletes_groups ag on ag.athlete_competition_id = ac.id
left join athletes a on a.id = ag.athlete_id
where c.deleted_at is null
group by c.id"""

sql_string_coach = """select c.id as "id", c.name as "name", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
from competitions c
left join tournaments t on t.competition_id = c.id
left join matches m on m.tournament_id = t.id
left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
left join athletes_groups ag on ag.athlete_competition_id = ac.id
left join athletes a on a.id = ag.athlete_id
where c.deleted_at is null
    and c.show_public = true
group by c.id"""

sql_string_anon = f"""select c.id as "id", c.name as "name", count(distinct m.id) as "matches", count(distinct a.id) as "athletes"
from competitions c
left join tournaments t on t.competition_id = c.id
left join matches m on m.tournament_id = t.id
left join athlete_competitions ac on m.athlete_red_id = ac.id or m.athlete_blue_id = ac.id
left join athletes_groups ag on ag.athlete_competition_id = ac.id
left join athletes a on a.id = ag.athlete_id
where c.deleted_at is null
    and c.show_public = true
    and c.competition_end + '{timedelta(days=1)}' < '{datetime.today()}'
group by c.id"""

sql_string_direct_winners = """select tab1.competition_id as "competition_id", sum(tab1.direct_winners) as "direct_winners"
from (select c.id as "competition_id", c.name as "competition_name", t.id, sum(case when m.athlete_blue_id is null and m.athlete_red_id is not null then 1 else 0 end) as "direct_winners"
from competitions c 
left join tournaments t on t.competition_id = c.id 
left join matches m on m.tournament_id = t.id
group by t.id, c.id
having count(t.id) = 1) as tab1
group by tab1.competition_id"""

result = db.execute(text(sql_string_admin))
direct_winners_result = db.execute(text(sql_string_direct_winners))
return_data = []
for r in result:
    for w in direct_winners_result:
        if str(w["competition_id"]) == str(r["id"]):
            return_data.append(
                {
                    "name": r["name"],
                    "id": str(r["id"]),
                    "tournaments": r["tournaments"],
                    "matches": r["matches"],
                    "direct_winners": int(w["direct_winners"]),
                    "athletes": r["athletes"],
                }
            )
            break

json_formatted_str = json.dumps(return_data, indent=4)
#print(json_formatted_str)

coach_result = db.execute(text(sql_string_coach))
coach_data = []
for r in coach_result:
    coach_data.append(
        {
            "name": r["name"],
            "id": str(r["id"]),
            "matches": r["matches"],
            "athletes": r["athletes"],
        }
    )

coach_data_formatted = json.dumps(coach_data, indent=4)
print(coach_data_formatted)

anon_result = db.execute(text(sql_string_anon))
anon_data = []
for r in anon_result:
    anon_data.append(
        {
            "name": r["name"],
            "id": str(r["id"]),
            "matches": r["matches"],
            "athletes": r["athletes"],
        }
    )

anon_data_formatted = json.dumps(anon_data, indent=4)
print(anon_data_formatted)