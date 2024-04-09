from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from core.environment import config
from routes.authentication import auth_router
from routes.user import user_router
from routes.athlete import athlete_router
from routes.competition import competition_router
from routes.athlete_competition import athlete_competition_router
from routes.match import match_router
from routes.tournament import tournament_router
from routes.category import category_router
from routes.team import team_router
from routes.belt import belt_router
from routes.athlete_group import athlete_group_router
from routes.inscription import inscription_router
from routes.category_type import category_type_router
from routes.insurance_type import insurance_type_router
from routes.insurance_group import insurance_group_router
from routes.insurance import insurance_router
from routes.private_info import private_info_router
from routes.identification_document import identification_document_router
from routes.responsible import responsible_router
from routes.address import address_router
from routes.penalization import penalization_router

# app = FastAPI(docs_url="/docs", redoc_url=None)
app = FastAPI(docs_url=None, redoc_url=None)

ORIGINS = config.get("cors.allowed")
origins = ORIGINS.split(",")
origins.append("*")
print("\nCORS ORIGINS: ")
for o in origins:
    print("\t" + o)
print("END ORIGINS\n")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# Includes all app routers in the app

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(athlete_router)

app.include_router(team_router)

app.include_router(competition_router)

app.include_router(athlete_competition_router)

app.include_router(match_router)

app.include_router(tournament_router)

app.include_router(category_router)

app.include_router(category_type_router)

app.include_router(belt_router)

app.include_router(athlete_group_router)

app.include_router(inscription_router)

app.include_router(insurance_type_router)

app.include_router(insurance_group_router)

app.include_router(insurance_router)

app.include_router(private_info_router)

app.include_router(identification_document_router)

app.include_router(responsible_router)

app.include_router(address_router)

app.include_router(penalization_router)
