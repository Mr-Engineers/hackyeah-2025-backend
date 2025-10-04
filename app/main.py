from fastapi import FastAPI
from app.player_state.router import router as player_router
from app.simulation.router import router as simulation_router

app = FastAPI(
    title="Life Simulation API",
    version="0.1.0",
    description="API do symulacji życia gracza"
)

app.include_router(player_router)
app.include_router(simulation_router)

@app.get("/")
def root():
    return {"message": "Life Simulation API działa 🚀"}
