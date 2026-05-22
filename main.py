from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routes import markets, admin, bets, portfolio
from scheduler.cron import start_scheduler, shutdown_scheduler

app = FastAPI(title="Agora Backend API", description="African Macro Prediction Markets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(markets.router)
app.include_router(admin.router)
app.include_router(bets.router)
app.include_router(portfolio.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()
