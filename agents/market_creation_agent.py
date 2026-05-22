import uuid
from datetime import datetime, timezone
from utils.news_fetcher import get_latest_macro_news
from integrations.ai_client import get_claude_json_completion
from db.supabase_client import supabase

SYSTEM_PROMPT = """You are the Chief Market Architect for Agora, an institutional prediction market platform. 
Your goal is to propose exactly 3 highly relevant, high-volume prediction markets based on current global and African macro news.
You must return a JSON object with a "markets" array containing exactly 3 markets.
Mandatory: At least 1 market must be a Global Macro event, and at least 1 must be a Deep-Dive African Macro event.

JSON Structure:
{
  "markets": [
    {
      "title": "String (Short, punchy question)",
      "description": "String (Detailed context)",
      "vertical": "String (one of: nigerian_macro, african_macro, global_macro)",
      "resolution_criteria": "String (Unambiguous criteria for yes/no resolution)",
      "source_of_truth": "String (URL or name of official body)",
      "probability_yes": Float (Between 0.01 and 0.99),
      "closes_at": "String (ISO-8601 datetime, e.g. 2026-12-31T23:59:59Z)"
    }
  ]
}
"""

def run_market_creation():
    print("Agent 1: Running Market Creation Pipeline...")
    news = get_latest_macro_news()
    
    prompt = f"Here is the latest macro news. Propose 3 new prediction markets:\n\n{news}"
    
    print("Agent 1: Calling Claude 3.5 Sonnet...")
    response_json = get_claude_json_completion(prompt, SYSTEM_PROMPT)
    
    if not response_json or "markets" not in response_json:
        print("Agent 1: Failed to get valid response from Claude.")
        return
        
    markets_to_insert = []
    now = datetime.now(timezone.utc).isoformat()
    
    for m in response_json["markets"]:
        market_data = {
            "id": str(uuid.uuid4()),
            "title": m["title"],
            "description": m["description"],
            "vertical": m["vertical"],
            "resolution_criteria": m["resolution_criteria"],
            "source_of_truth": m["source_of_truth"],
            "probability_yes": m["probability_yes"],
            "status": "draft",  # Always draft initially
            "closes_at": m["closes_at"],
            "created_by": "ai_agent_1",
            "total_yes_usdc": 0,
            "total_no_usdc": 0,
            "created_at": now
        }
        markets_to_insert.append(market_data)
        
    print(f"Agent 1: Generated {len(markets_to_insert)} draft markets. Inserting to Supabase...")
    
    for m in markets_to_insert:
        try:
            supabase.table("markets").insert(m).execute()
            print(f"Agent 1: Inserted draft market - {m['title']}")
        except Exception as e:
            print(f"Agent 1: Error inserting market {m['title']}: {e}")
            
    print("Agent 1: Run complete.")

if __name__ == "__main__":
    run_market_creation()
