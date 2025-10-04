from fastapi import FastAPI
from app.player_state.router import router as player_router
from app.simulation.router import router as simulation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Life Simulation API",
    version="0.1.0",
    description="API do symulacji życia gracza"
)

app.include_router(player_router)
app.include_router(simulation_router)

# Dodajemy CORS, żeby frontend mógł odbierać dane z innego portu
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/")
def root():
    return {"message": "Life Simulation API działa 🚀"}
