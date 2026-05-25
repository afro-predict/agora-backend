from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from services.orders_service import OrdersService

# We'll map two routers here, one for /markets/{id}/bet and one for /bets
router = APIRouter(tags=["bets"])

class BetRequest(BaseModel):
    outcome: str
    amount_usdc: float
    wallet_address: str

class TopLevelBetRequest(BetRequest):
    market_id: str

@router.post("/markets/{market_id}/bet")
async def place_bet(
    bet_req: BetRequest,
    market_id: str = Path(..., description="The ID of the market to bet on")
):
    try:
        if bet_req.amount_usdc <= 0:
            raise ValueError("Bet amount must be greater than 0")
            
        data = OrdersService.place_order(
            market_id=market_id,
            wallet_address=bet_req.wallet_address,
            outcome=bet_req.outcome.lower(),
            amount_usdc=bet_req.amount_usdc
        )
        
        return {
            "success": True,
            "data": data,
            "error": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))

@router.post("/bets")
async def place_top_level_bet(req: TopLevelBetRequest):
    try:
        if req.amount_usdc <= 0:
            raise ValueError("Bet amount must be greater than 0")
            
        data = OrdersService.place_order(
            market_id=req.market_id,
            wallet_address=req.wallet_address,
            outcome=req.outcome.lower(),
            amount_usdc=req.amount_usdc
        )
        
        return {
            "success": True,
            "data": data,
            "error": None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))
