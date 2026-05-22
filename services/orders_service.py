import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from db.supabase_client import supabase

class OrdersService:
    @staticmethod
    def place_order(market_id: str, wallet_address: str, outcome: str, amount_usdc: float) -> Dict[str, Any]:
        # 1. Fetch market
        resp = supabase.table("markets").select("*").eq("id", market_id).execute()
        if not resp.data:
            raise ValueError("Market not found")
            
        market_data = resp.data[0]
        
        # 2. Validate market
        now = datetime.now(timezone.utc)
        closes_at = datetime.fromisoformat(market_data["closes_at"])
        if market_data["status"] != "open" or closes_at <= now:
            raise ValueError("Market is not open for trading")
            
        if outcome not in ["yes", "no"]:
            raise ValueError("Invalid outcome. Must be 'yes' or 'no'")
            
        # 3. Calculate probability & payout
        prob_yes = market_data["probability_yes"]
        implied_prob = prob_yes if outcome == "yes" else (1.0 - prob_yes)
        
        if implied_prob <= 0.01:
            implied_prob = 0.01
            
        potential_payout = round(amount_usdc / implied_prob, 2)
        
        # 4. Generate IDs and Timestamps
        order_id = str(uuid.uuid4())
        timestamp = now.isoformat()
        
        # 5. Insert Order
        order_data = {
            "id": order_id,
            "market_id": market_id,
            "wallet_address": wallet_address,
            "outcome": outcome,
            "amount_usdc": amount_usdc,
            "potential_payout": potential_payout,
            "implied_probability": implied_prob,
            "created_at": timestamp
        }
        supabase.table("orders").insert(order_data).execute()
        
        # 6. Update Market Volume
        new_yes_volume = market_data["total_yes_usdc"] + (amount_usdc if outcome == "yes" else 0)
        new_no_volume = market_data["total_no_usdc"] + (amount_usdc if outcome == "no" else 0)
        
        supabase.table("markets").update({
            "total_yes_usdc": new_yes_volume,
            "total_no_usdc": new_no_volume
        }).eq("id", market_id).execute()
        
        # 7. Update User Position (Upsert)
        pos_resp = supabase.table("positions").select("*").eq("market_id", market_id).eq("wallet_address", wallet_address).eq("outcome", outcome).execute()
        
        if pos_resp.data:
            pos = pos_resp.data[0]
            supabase.table("positions").update({
                "amount_usdc": pos["amount_usdc"] + amount_usdc,
                "potential_payout": pos["potential_payout"] + potential_payout,
                "updated_at": timestamp
            }).eq("id", pos["id"]).execute()
        else:
            supabase.table("positions").insert({
                "id": str(uuid.uuid4()),
                "wallet_address": wallet_address,
                "market_id": market_id,
                "outcome": outcome,
                "amount_usdc": amount_usdc,
                "potential_payout": potential_payout,
                "created_at": timestamp,
                "updated_at": timestamp
            }).execute()
            
        # 8. Return formatted data
        return {
            "order_id": order_id,
            "market_id": market_id,
            "outcome": outcome,
            "amount_usdc": amount_usdc,
            "potential_payout": potential_payout,
            "implied_probability": implied_prob,
            "kelly_suggestion": {
                "recommended_fraction": 0.05,
                "recommended_amount_usdc": round(amount_usdc * 0.8, 2),
                "reasoning": "Mocked for Day 4. Agent 3 implementation pending."
            },
            "arc_tx_hash": f"0x_mock_tx_{order_id[:8]}",
            "settlement": "pending",
            "message": "Bet placed successfully. USDC held in escrow on Arc."
        }
