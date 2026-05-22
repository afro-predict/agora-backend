from fastapi import APIRouter, HTTPException, Path
from services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/{wallet_address}")
async def get_portfolio(wallet_address: str = Path(...)):
    try:
        data = PortfolioService.get_portfolio(wallet_address)
        return {
            "success": True,
            "data": data,
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
