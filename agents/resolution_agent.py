from datetime import datetime, timezone
from utils.news_fetcher import get_latest_macro_news
from integrations.ai_client import get_claude_json_completion
from db.supabase_client import supabase
from services.circle_service import CircleService

SYSTEM_PROMPT = """You are the Chief Resolution Officer (Agent 4) for Agora, a prediction market.
Your strict duty is to determine the final outcome of expired prediction markets based ONLY on provided news.
You will receive the market's title, its strict resolution criteria, and the latest news context.

If the news clearly answers the question based on the criteria, resolve it as "yes" or "no".
If the news is completely inconclusive, resolve it as "invalid" (though try your best to find a yes/no if possible).

You must return a JSON object containing the resolution data.

JSON Structure:
{
  "outcome": "yes" | "no" | "invalid",
  "confidence": "high" | "medium" | "low",
  "reasoning": "String (Detailed explanation of why this outcome was chosen based on the news and criteria)"
}
"""

def run_market_resolution():
    print("Agent 4: Running Settlement / Resolution Service...")
    
    # 1. Fetch expired open markets
    now_iso = datetime.now(timezone.utc).isoformat()
    response = supabase.table("markets").select("id, title, resolution_criteria").eq("status", "open").lte("closes_at", now_iso).execute()
    
    expired_markets = response.data
    if not expired_markets:
        print("Agent 4: No expired markets found to resolve.")
        return
        
    print(f"Agent 4: Found {len(expired_markets)} expired markets. Fetching news for resolution...")
    
    # 2. Fetch context
    news = get_latest_macro_news()
    
    # 3. Resolve each market
    for market in expired_markets:
        print(f"Agent 4: Resolving market '{market['title']}'...")
        prompt = f"""
        MARKET TITLE: {market['title']}
        RESOLUTION CRITERIA: {market['resolution_criteria']}
        
        LATEST NEWS CONTEXT:
        {news}
        
        Determine the outcome of this market.
        """
        
        resolution_data = get_claude_json_completion(prompt, SYSTEM_PROMPT)
        
        if not resolution_data or "outcome" not in resolution_data:
            print(f"Agent 4: Failed to get valid resolution for {market['id']}.")
            continue
            
        outcome = resolution_data["outcome"]
        if outcome not in ["yes", "no", "invalid"]:
            outcome = "invalid"
            
        print(f"Agent 4: Outcome determined -> {outcome.upper()}. Updating database...")
        
        # 4. Update Database
        try:
            supabase.table("markets").update({
                "status": "resolved",
                "outcome": outcome,
                "resolved_at": now_iso
            }).eq("id", market["id"]).execute()
            
            # Log the rationale so it shows up in the UI
            supabase.table("ai_rationale").insert({
                "market_id": market["id"],
                "probability_yes": 1.0 if outcome == "yes" else 0.0,
                "confidence": resolution_data.get("confidence", "high"),
                "rationale": f"FINAL RESOLUTION [{outcome.upper()}]: " + resolution_data.get("reasoning", ""),
                "key_factors": ["Market expired", "Settlement processing"],
                "risk_factors": ["Resolution finalized"],
                "sources": [],
                "data_snapshot": {},
                "generated_at": now_iso
            }).execute()
            
            print(f"Agent 4: Successfully resolved market {market['id']}.")
            
            # 5. Execute Payouts via Circle
            if outcome in ["yes", "no"]:
                print(f"Agent 4: Executing Circle payouts for winning '{outcome}' positions...")
                positions_resp = supabase.table("positions").select("*").eq("market_id", market["id"]).eq("outcome", outcome).execute()
                
                for pos in positions_resp.data:
                    payout_tx = CircleService.payout_winnings(pos["wallet_address"], pos["potential_payout"])
                    print(f"Agent 4: Paid {pos['potential_payout']} USDC to {pos['wallet_address']}. Tx: {payout_tx}")
            
        except Exception as e:
            print(f"Agent 4: Error updating database for {market['id']}: {e}")
            
    print("Agent 4: Settlement Service run complete.")

if __name__ == "__main__":
    run_market_resolution()
