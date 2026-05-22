from fastapi import APIRouter, HTTPException, BackgroundTasks
from agents.market_creation_agent import run_market_creation
from agents.probability_agent import run_probability_updates
from agents.resolution_agent import run_market_resolution

from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

class CreateMarketRequest(BaseModel):
    vertical: str
    trigger: str
    api_key: str

@router.post("/trigger-agents")
async def trigger_agents(background_tasks: BackgroundTasks):
    """
    Manually triggers both AI Agents to run in the background.
    Used for testing the AI integration without waiting for cron schedules.
    """
    try:
        background_tasks.add_task(run_market_creation)
        background_tasks.add_task(run_probability_updates)
        background_tasks.add_task(run_market_resolution)
        return {
            "success": True,
            "message": "AI Agents successfully triggered. Claude is working in the background! Please check the Railway logs or database in ~30 seconds."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/markets/create")
async def create_market(req: CreateMarketRequest):
    if req.api_key != "ADMIN_API_KEY":
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    try:
        # Note: We ignore vertical and trigger for the MVP and just let Claude decide based on latest news
        markets = run_market_creation()
        
        return {
            "success": True,
            "data": {
                "markets_created": len(markets),
                "markets": markets
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
