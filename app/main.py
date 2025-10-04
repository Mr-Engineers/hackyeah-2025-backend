from fastapi import FastAPI
from app.player_state import router

app = FastAPI(
    title="Life Simulation API",
    version="0.1.0",
    description="API do symulacji życia gracza"
)

app.include_router(router.router)


@app.get("/")
def root():
    return {"message": "Life Simulation API działa 🚀"}
