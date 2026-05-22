from fastapi import APIRouter, HTTPException, BackgroundTasks
from agents.market_creation_agent import run_market_creation
from agents.probability_agent import run_probability_updates

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/trigger-agents")
async def trigger_agents(background_tasks: BackgroundTasks):
    """
    Manually triggers both AI Agents to run in the background.
    Used for testing the AI integration without waiting for cron schedules.
    """
    try:
        background_tasks.add_task(run_market_creation)
        background_tasks.add_task(run_probability_updates)
        return {
            "success": True,
            "message": "AI Agents successfully triggered. Claude is working in the background! Please check the Railway logs or database in ~30 seconds."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
