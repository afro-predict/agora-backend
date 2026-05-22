from typing import List, Optional, Dict, Any
from db.supabase_client import supabase
from db.models import Market
from datetime import datetime, timezone

class MarketsService:
    @staticmethod
    def get_all_markets(vertical: Optional[str] = None, status: Optional[str] = None, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        query = supabase.table("markets").select("*")
        
        now = datetime.now(timezone.utc)
        
        if vertical:
            query = query.eq("vertical", vertical)
            
        if status == "open":
            query = query.eq("status", "open").gt("closes_at", now.isoformat())
        elif status == "closed":
            query = query.or_(f"status.eq.closed,closes_at.lte.{now.isoformat()}")
        elif status:
            query = query.eq("status", status)
            
        response = query.order("closes_at").range(offset, offset + limit - 1).execute()
        markets_data = response.data
        
        markets = [Market(**m) for m in markets_data]
        
        # Calculate by_vertical aggregations roughly
        all_markets_resp = supabase.table("markets").select("vertical").execute()
        by_vertical = {}
        for row in all_markets_resp.data:
            v = row["vertical"]
            by_vertical[v] = by_vertical.get(v, 0) + 1
            
        formatted_markets = []
        for m in markets:
            is_expired = m.closes_at <= now
            display_status = "closed" if (m.status == "open" and is_expired) else m.status
            hours_remaining = max(0, int((m.closes_at - now).total_seconds() / 3600))
            formatted_markets.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "vertical": m.vertical,
                "probability_yes": m.probability_yes,
                "probability_no": m.probability_no,
                "total_yes_usdc": m.total_yes_usdc,
                "total_no_usdc": m.total_no_usdc,
                "total_volume_usdc": m.total_volume_usdc,
                "status": display_status,
                "closes_at": m.closes_at.isoformat(),
                "hours_remaining": hours_remaining,
                "last_probability_update": m.probability_updated_at.isoformat() if m.probability_updated_at else m.created_at.isoformat()
            })
            
        return {
            "markets": formatted_markets,
            "total": len(all_markets_resp.data),
            "by_vertical": by_vertical
        }

    @staticmethod
    def get_market_detail(market_id: str) -> Optional[Dict[str, Any]]:
        response = supabase.table("markets").select("*").eq("id", market_id).execute()
        if not response.data:
            return None
            
        market = Market(**response.data[0])
        
        # Get order book (recent orders)
        orders_resp = supabase.table("orders").select("outcome, amount_usdc, created_at").eq("market_id", market_id).order("created_at", desc=True).limit(50).execute()
        yes_orders = []
        no_orders = []
        for o in orders_resp.data:
            order_data = {"amount_usdc": o["amount_usdc"], "placed_at": o["created_at"]}
            if o["outcome"] == "yes":
                yes_orders.append(order_data)
            else:
                no_orders.append(order_data)
                
        # Get probability history
        rationale_resp = supabase.table("ai_rationale").select("probability_yes, generated_at").eq("market_id", market_id).order("generated_at", desc=True).limit(10).execute()
        prob_history = []
        for r in rationale_resp.data:
            prob_history.append({
                "probability_yes": r["probability_yes"],
                "timestamp": r["generated_at"]
            })
            
        is_expired = market.closes_at <= datetime.now(timezone.utc)
        display_status = "closed" if (market.status == "open" and is_expired) else market.status

        return {
            "market": {
                "id": market.id,
                "title": market.title,
                "description": market.description,
                "vertical": market.vertical,
                "resolution_criteria": market.resolution_criteria,
                "source_of_truth": market.source_of_truth,
                "probability_yes": market.probability_yes,
                "probability_no": market.probability_no,
                "status": display_status,
                "closes_at": market.closes_at.isoformat(),
                "total_yes_usdc": market.total_yes_usdc,
                "total_no_usdc": market.total_no_usdc
            },
            "order_book": {
                "yes_orders": yes_orders,
                "no_orders": no_orders
            },
            "probability_history": prob_history
        }

    @staticmethod
    def get_ai_rationale(market_id: str) -> Optional[Dict[str, Any]]:
        # Fetch the most recent rationale for this market
        response = supabase.table("ai_rationale").select("*").eq("market_id", market_id).order("generated_at", desc=True).limit(1).execute()
        if not response.data:
            return None
            
        r = response.data[0]
        market_resp = supabase.table("markets").select("title").eq("id", market_id).execute()
        market_title = market_resp.data[0]["title"] if market_resp.data else "Unknown Market"
        
        return {
            "market_id": market_id,
            "market_title": market_title,
            "probability_yes": r["probability_yes"],
            "confidence": r.get("confidence", "medium"),
            "generated_at": r["generated_at"],
            "rationale": r["rationale"],
            "key_factors": r.get("key_factors", []),
            "risk_factors": r.get("risk_factors", []),
            "sources": r.get("sources", []),
            "data_snapshot": r.get("data_snapshot", {})
        }
