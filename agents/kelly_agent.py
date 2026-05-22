from integrations.ai_client import get_claude_json_completion

SYSTEM_PROMPT = """You are the Quantitative Risk Manager for Agora, advising a retail trader.
Your goal is to evaluate their intended prediction market bet using the Kelly Criterion and provide an institutional-grade risk assessment.
You will be provided with:
- The market's "true probability" (as calculated by our AI models)
- The market's "implied probability" (current market odds)
- The user's intended bet amount in USDC
- The user's estimated total bankroll in USDC

Calculate the optimal Kelly fraction.
If the intended bet amount exceeds the Kelly recommendation, warn the user.
If the intended bet is within safe limits, validate their risk management.

Return exactly this JSON structure:
{
  "recommended_fraction": Float (e.g. 0.05 for 5%),
  "recommended_amount_usdc": Float,
  "reasoning": "String (A concise 2-sentence explanation of the risk vs reward for this specific trade)"
}
"""

def get_kelly_suggestion(true_prob: float, implied_prob: float, amount_usdc: float, bankroll_usdc: float = 1000.0) -> dict:
    prompt = f"""
    Evaluate this bet:
    True Probability: {true_prob}
    Implied Probability (Market Price): {implied_prob}
    Intended Bet: ${amount_usdc} USDC
    User's Total Bankroll: ${bankroll_usdc} USDC
    """
    
    response = get_claude_json_completion(prompt, SYSTEM_PROMPT)
    if not response or "reasoning" not in response:
        # Fallback if Claude fails
        return {
            "recommended_fraction": 0.05,
            "recommended_amount_usdc": bankroll_usdc * 0.05,
            "reasoning": "Standard 5% portfolio risk cap applied."
        }
    return response
