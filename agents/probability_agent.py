import uuid
from datetime import datetime, timezone
from utils.news_fetcher import get_latest_macro_news
from integrations.ai_client import get_claude_json_completion
from db.supabase_client import supabase

SYSTEM_PROMPT = """You are the Quantitative Risk Manager for Agora.
Your goal is to re-evaluate the true probability of prediction markets resolving to YES based on breaking news.
You will be given a list of open markets and the latest news.
For each market, calculate the new `probability_yes` (a float between 0.01 and 0.99) and provide a concise 2-sentence rationale.

Return a JSON object in this structure:
{
  "updates": [
    {
      "market_id": "String (exact ID passed to you)",
      "new_probability_yes": Float,
      "rationale": "String"
    }
  ]
}
"""

def run_probability_updates():
    print("Agent 2: Running Probability Update Pipeline...")
    
    # 1. Fetch all OPEN markets
    print("Agent 2: Fetching open markets from Supabase...")
    response = supabase.table("markets").select("id, title, description, probability_yes").eq("status", "open").execute()
    open_markets = response.data
    
    if not open_markets:
        print("Agent 2: No open markets to update.")
        return
        
    print(f"Agent 2: Found {len(open_markets)} open markets.")
    
    # 2. Fetch news
    news = get_latest_macro_news()
    
    # 3. Construct prompt
    prompt = f"Here is the latest macro news:\n\n{news}\n\nHere are the open markets:\n"
    for m in open_markets:
        prompt += f"- ID: {m['id']} | Title: {m['title']} | Current Prob: {m['probability_yes']}\n"
        
    prompt += "\nPlease evaluate and provide updated probabilities and rationales for all of these markets."
    
    # 4. Call Claude
    print("Agent 2: Calling Claude 3.5 Sonnet to evaluate probabilities...")
    response_json = get_claude_json_completion(prompt, SYSTEM_PROMPT)
    
    if not response_json or "updates" not in response_json:
        print("Agent 2: Failed to get valid response from Claude.")
        return
        
    # 5. Update markets and log rationale
    now = datetime.now(timezone.utc).isoformat()
    updates = response_json["updates"]
    
    print(f"Agent 2: Received {len(updates)} probability updates. Writing to DB...")
    
    for update in updates:
        market_id = update["market_id"]
        new_prob = update["new_probability_yes"]
        rationale_text = update["rationale"]
        
        try:
            # Update the market
            supabase.table("markets").update({
                "probability_yes": new_prob,
                "probability_updated_at": now
            }).eq("id", market_id).execute()
            
            # Log the rationale
            rationale_data = {
                "id": str(uuid.uuid4()),
                "market_id": market_id,
                "probability_yes": new_prob,
                "rationale": rationale_text,
                "generated_at": now,
                "model_used": "claude-3.5-sonnet"
            }
            supabase.table("ai_rationale").insert(rationale_data).execute()
            print(f"Agent 2: Updated market {market_id} to {new_prob*100}%")
        except Exception as e:
            print(f"Agent 2: Error updating market {market_id}: {e}")
            
    print("Agent 2: Run complete.")

if __name__ == "__main__":
    run_probability_updates()
