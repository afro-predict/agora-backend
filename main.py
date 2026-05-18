import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Agora Backend API", description="African Macro Prediction Markets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_API_DIR = os.path.join(os.path.dirname(__file__), "mock-api")

def read_mock_json(filename: str):
    path = os.path.join(MOCK_API_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Mock file not found")

@app.get("/markets")
async def get_markets(vertical: Optional[str] = None, status: Optional[str] = None, limit: int = 20, offset: int = 0):
    return read_mock_json("markets.json")

@app.get("/markets/{market_id}")
async def get_market_detail(market_id: str):
    return read_mock_json("market-detail.json")

class BetRequest(BaseModel):
    outcome: str
    amount_usdc: float
    wallet_address: str

@app.post("/markets/{market_id}/bet")
async def place_bet(market_id: str, bet: BetRequest):
    return read_mock_json("bet-response.json")

@app.get("/portfolio/{wallet_address}")
async def get_portfolio(wallet_address: str):
    return read_mock_json("portfolio.json")

@app.get("/markets/{market_id}/ai-rationale")
async def get_ai_rationale(market_id: str):
    return read_mock_json("ai-rationale.json")

class CreateMarketRequest(BaseModel):
    vertical: str
    trigger: str
    api_key: str

@app.post("/markets/create")
async def create_market(req: CreateMarketRequest):
    return {
      "success": True,
      "data": {
        "markets_created": 2,
        "markets": [
          {
            "id": "uuid",
            "title": "Will Nigeria's May 2026 CPI exceed 34%?",
            "vertical": "nigerian_macro",
            "resolution_criteria": "Resolution YES if NBS official CPI release for May 2026 states headline inflation exceeds 34.0%.",
            "closes_at": "2026-06-15T12:00:00Z",
            "initial_probability_yes": 0.61
          }
        ]
      },
      "error": None,
      "timestamp": "2026-05-17T10:00:00Z"
    }
