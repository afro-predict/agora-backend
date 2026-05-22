import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("WARNING: ANTHROPIC_API_KEY is not set.")

# Pass empty string if none so it doesn't crash on import, it will crash on use
anthropic_client = Anthropic(api_key=api_key or "missing")

def get_claude_json_completion(prompt: str, system_prompt: str) -> dict:
    """Helper to get a JSON response from Claude 3.5 Sonnet"""
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Claude might wrap JSON in markdown block
        text = response.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"Error calling Anthropic: {e}")
        return None
