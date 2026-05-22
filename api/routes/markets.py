from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timezone
from services.markets_service import MarketsService

router = APIRouter(prefix="/markets", tags=["markets"])

@router.get("")
async def get_markets(
    vertical: Optional[str] = Query(None),
    status: Optional[str] = Query("open"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    try:
        data = MarketsService.get_all_markets(vertical, status, limit, offset)
        return {
            "success": True,
            "data": data,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{market_id}")
async def get_market_detail(market_id: str):
    try:
        data = MarketsService.get_market_detail(market_id)
        if not data:
            return {
                "success": False,
                "data": None,
                "error": "Market not found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        return {
            "success": True,
            "data": data,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{market_id}/ai-rationale")
async def get_ai_rationale(market_id: str):
    try:
        data = MarketsService.get_ai_rationale(market_id)
        if not data:
            return {
                "success": False,
                "data": None,
                "error": "AI Rationale not found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        return {
            "success": True,
            "data": data,
            "error": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
