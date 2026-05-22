from typing import Dict, Any
from db.supabase_client import supabase

class PortfolioService:
    @staticmethod
    def get_portfolio(wallet_address: str) -> Dict[str, Any]:
        orders_resp = supabase.table("orders").select("amount_usdc").eq("wallet_address", wallet_address).execute()
        total_wagered = sum(o["amount_usdc"] for o in orders_resp.data)
        
        positions_resp = supabase.table("positions").select("*").eq("wallet_address", wallet_address).execute()
        
        if not positions_resp.data:
            return {
                "wallet_address": wallet_address,
                "summary": {
                    "total_wagered_usdc": total_wagered, 
                    "total_won_usdc": 0, 
                    "total_lost_usdc": 0,
                    "open_exposure_usdc": 0, 
                    "net_pnl_usdc": 0, 
                    "win_rate": 0
                },
                "open_positions": [],
                "resolved_positions": []
            }
            
        market_ids = list(set([p["market_id"] for p in positions_resp.data]))
        markets_resp = supabase.table("markets").select("id, title, probability_yes, status, closes_at, outcome").in_("id", market_ids).execute()
        markets_map = {m["id"]: m for m in markets_resp.data}
        
        open_positions = []
        resolved_positions = []
        total_won = 0
        total_lost = 0
        open_exposure = 0
        wins = 0
        losses = 0
        
        for p in positions_resp.data:
            market = markets_map.get(p["market_id"])
            if not market: continue
            
            if market["status"] == "resolved":
                if market["outcome"] == p["outcome"]:
                    pnl = p["potential_payout"] - p["amount_usdc"]
                    total_won += p["potential_payout"]
                    result = "won"
                    wins += 1
                else:
                    pnl = -p["amount_usdc"]
                    total_lost += p["amount_usdc"]
                    result = "lost"
                    losses += 1
                    
                resolved_positions.append({
                    "market_id": market["id"],
                    "market_title": market["title"],
                    "outcome": p["outcome"],
                    "amount_usdc": p["amount_usdc"],
                    "result": result,
                    "pnl_usdc": pnl,
                    "arc_payout_tx": f"0x_mock_{p['id'][:8]}",
                    "resolved_at": market["closes_at"]
                })
            else:
                open_exposure += p["amount_usdc"]
                open_positions.append({
                    "market_id": market["id"],
                    "market_title": market["title"],
                    "outcome": p["outcome"],
                    "amount_usdc": p["amount_usdc"],
                    "current_probability": market["probability_yes"],
                    "potential_payout": p["potential_payout"],
                    "closes_at": market["closes_at"]
                })
                
        net_pnl = total_won - total_lost
        total_resolved = wins + losses
        win_rate = (wins / total_resolved) if total_resolved > 0 else 0
        
        return {
            "wallet_address": wallet_address,
            "summary": {
                "total_wagered_usdc": total_wagered,
                "total_won_usdc": total_won,
                "total_lost_usdc": total_lost,
                "open_exposure_usdc": open_exposure,
                "net_pnl_usdc": net_pnl,
                "win_rate": round(win_rate, 2)
            },
            "open_positions": open_positions,
            "resolved_positions": resolved_positions
        }
