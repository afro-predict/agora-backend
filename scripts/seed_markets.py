import os
import sys
import uuid
from datetime import datetime, timezone

# Ensure we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.supabase_client import supabase

MARKETS = [
    # Vertical 1: Nigerian Macro
    {
        "id": str(uuid.uuid4()),
        "title": "Will CBN hold rates above 26.5% at the May MPC?",
        "description": "The Central Bank of Nigeria (CBN) Monetary Policy Committee meets to decide on interest rates. Will they maintain or hike the MPR above 26.5%?",
        "vertical": "nigerian_macro",
        "resolution_criteria": "Resolution YES if the official CBN MPC communique on May 20, 2026 announces a Monetary Policy Rate (MPR) of 26.5% or higher.",
        "source_of_truth": "https://www.cbn.gov.ng/",
        "probability_yes": 0.73,
        "status": "open",
        "closes_at": "2026-05-20T14:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 12500.00,
        "total_no_usdc": 4200.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Will Nigeria CPI exceed 33% in April?",
        "description": "Headline inflation in Nigeria has been surging. Will the April CPI reading exceed 33% year-on-year?",
        "vertical": "nigerian_macro",
        "resolution_criteria": "Resolution YES if the NBS official April CPI report released in May shows headline inflation > 33.0%.",
        "source_of_truth": "https://nigerianstat.gov.ng/",
        "probability_yes": 0.85,
        "status": "open",
        "closes_at": "2026-05-15T10:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 8400.00,
        "total_no_usdc": 1200.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Naira parallel market rate below 1400/$ by June?",
        "description": "Will the Nigerian Naira strengthen below 1400 NGN per USD on the parallel market by the end of June 2026?",
        "vertical": "nigerian_macro",
        "resolution_criteria": "Resolution YES if AbokiFX or Nairametrics reports a parallel market closing rate < 1400 NGN/USD on June 30, 2026.",
        "source_of_truth": "https://nairametrics.com/",
        "probability_yes": 0.45,
        "status": "open",
        "closes_at": "2026-06-30T16:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 25000.00,
        "total_no_usdc": 32000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Nigeria Q1 GDP Growth > 3.0%?",
        "description": "Will Nigeria's Gross Domestic Product grow by more than 3.0% year-on-year in the first quarter of 2026?",
        "vertical": "nigerian_macro",
        "resolution_criteria": "Resolution YES if the NBS Q1 2026 GDP report shows real GDP growth > 3.0%.",
        "source_of_truth": "https://nigerianstat.gov.ng/",
        "probability_yes": 0.55,
        "status": "open",
        "closes_at": "2026-06-20T08:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 4000.00,
        "total_no_usdc": 3500.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # Vertical 2: African & EM Macro
    {
        "id": str(uuid.uuid4()),
        "title": "Will IMF approve Nigeria's requested program?",
        "description": "Will the International Monetary Fund approve a formal financial support program for Nigeria by the end of June?",
        "vertical": "african_macro",
        "resolution_criteria": "Resolution YES if the IMF Executive Board formally approves a lending arrangement for Nigeria by June 30, 2026.",
        "source_of_truth": "https://www.imf.org/",
        "probability_yes": 0.35,
        "status": "open",
        "closes_at": "2026-06-30T23:59:59Z",
        "created_by": "system",
        "total_yes_usdc": 10500.00,
        "total_no_usdc": 19000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Ghana CPI below 20% in May?",
        "description": "Will Ghana's headline inflation rate fall below 20% year-on-year in May 2026?",
        "vertical": "african_macro",
        "resolution_criteria": "Resolution YES if Ghana Statistical Service reports May 2026 CPI < 20.0%.",
        "source_of_truth": "https://statsghana.gov.gh/",
        "probability_yes": 0.60,
        "status": "open",
        "closes_at": "2026-06-10T10:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 2200.00,
        "total_no_usdc": 1500.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "South Africa Reserve Bank rate cut in May?",
        "description": "Will the SARB cut its repo rate at the May 2026 meeting?",
        "vertical": "african_macro",
        "resolution_criteria": "Resolution YES if SARB announces a reduction in the repo rate on May 29, 2026.",
        "source_of_truth": "https://www.resbank.co.za/",
        "probability_yes": 0.25,
        "status": "open",
        "closes_at": "2026-05-29T14:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 5000.00,
        "total_no_usdc": 15000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Kenya Shilling depreciates past 140/USD?",
        "description": "Will the Kenyan Shilling officially depreciate past 140 KES per USD by end of June 2026?",
        "vertical": "african_macro",
        "resolution_criteria": "Resolution YES if CBK official exchange rate exceeds 140.00 KES/USD on June 30, 2026.",
        "source_of_truth": "https://www.centralbank.go.ke/",
        "probability_yes": 0.40,
        "status": "open",
        "closes_at": "2026-06-30T16:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 7000.00,
        "total_no_usdc": 9000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # Vertical 3: Global Macro
    {
        "id": str(uuid.uuid4()),
        "title": "Fed rate cut at June FOMC meeting?",
        "description": "Will the US Federal Reserve cut the federal funds target rate at the June FOMC meeting?",
        "vertical": "global_macro",
        "resolution_criteria": "Resolution YES if FOMC announces a rate cut on June 12, 2026.",
        "source_of_truth": "https://www.federalreserve.gov/",
        "probability_yes": 0.15,
        "status": "open",
        "closes_at": "2026-06-12T18:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 45000.00,
        "total_no_usdc": 210000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "title": "IMF downgrades global growth forecast?",
        "description": "Will the IMF downgrade its 2026 global growth forecast in the upcoming WEO update?",
        "vertical": "global_macro",
        "resolution_criteria": "Resolution YES if the IMF World Economic Outlook update in June 2026 shows a lower global growth rate than the previous report.",
        "source_of_truth": "https://www.imf.org/en/Publications/WEO",
        "probability_yes": 0.70,
        "status": "open",
        "closes_at": "2026-06-25T13:00:00Z",
        "created_by": "system",
        "total_yes_usdc": 18000.00,
        "total_no_usdc": 7000.00,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

def seed_markets():
    print("Seeding markets to Supabase...")
    for market in MARKETS:
        # Check if already exists
        response = supabase.table("markets").select("id").eq("title", market["title"]).execute()
        if len(response.data) > 0:
            print(f"Market already exists: {market['title']}")
            continue
            
        print(f"Inserting: {market['title']}")
        supabase.table("markets").insert(market).execute()
        
    print("Seed complete!")

if __name__ == "__main__":
    seed_markets()
