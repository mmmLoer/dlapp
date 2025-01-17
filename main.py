from fastapi import FastAPI
from routes import players, teams, teamlists, matches, tournaments

app = FastAPI(title="Aplication API", version="1.0")

app.include_router(players.router, tags=["Players"])
app.include_router(teams.router, tags=["Teams"])
app.include_router(teamlists.router, tags=["TeamLists"])
app.include_router(matches.router, tags=["Matches"])
app.include_router(tournaments.router, tags=["Tournaments"])

@app.get("/")
def root():
    return {"message": "Welcome to the NSHUB APP API!"}
