# Agora API Contract

This document outlines the API responses for the Agora backend.

All responses follow this envelope:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2026-05-17T10:00:00Z"
}
```

## GET /markets

Returns all markets grouped by vertical.

Query params: `?vertical=nigerian_macro` `?status=open` `?limit=20` `?offset=0`

```json
{
  "success": true,
  "data": {
    "markets": [
      {
        "id": "uuid",
        "title": "Will CBN hold rates above 26.5% at the May 2026 MPC?",
        "description": "The CBN Monetary Policy Committee meets May 19-20...",
        "vertical": "nigerian_macro",
        "probability_yes": 0.73,
        "probability_no": 0.27,
        "total_yes_usdc": 4200.00,
        "total_no_usdc": 1580.00,
        "total_volume_usdc": 5780.00,
        "status": "open",
        "closes_at": "2026-05-20T14:00:00Z",
        "hours_remaining": 68,
        "last_probability_update": "2026-05-17T06:00:00Z"
      }
    ],
    "total": 12,
    "by_vertical": {
      "nigerian_macro": 4,
      "african_macro": 5,
      "global_macro": 3
    }
  }
}
```

## GET /markets/:id

Full market detail including order book and probability history.

```json
{
  "success": true,
  "data": {
    "market": {
      "id": "uuid",
      "title": "Will CBN hold rates above 26.5% at the May 2026 MPC?",
      "description": "The CBN Monetary Policy Committee meets May 19-20 2026...",
      "vertical": "nigerian_macro",
      "resolution_criteria": "Resolution YES if CBN's official post-MPC communiqué states the MPR is set at or above 26.5%. Resolution NO if MPR is set below 26.5%.",
      "source_of_truth": "CBN official press release at cbn.gov.ng",
      "probability_yes": 0.73,
      "probability_no": 0.27,
      "status": "open",
      "closes_at": "2026-05-20T14:00:00Z",
      "total_yes_usdc": 4200.00,
      "total_no_usdc": 1580.00
    },
    "order_book": {
      "yes_orders": [
        { "amount_usdc": 500, "placed_at": "2026-05-17T08:00:00Z" },
        { "amount_usdc": 250, "placed_at": "2026-05-17T07:30:00Z" }
      ],
      "no_orders": [
        { "amount_usdc": 300, "placed_at": "2026-05-17T09:00:00Z" }
      ]
    },
    "probability_history": [
      { "probability_yes": 0.68, "timestamp": "2026-05-15T06:00:00Z" },
      { "probability_yes": 0.71, "timestamp": "2026-05-16T06:00:00Z" },
      { "probability_yes": 0.73, "timestamp": "2026-05-17T06:00:00Z" }
    ]
  }
}
```

## POST /markets/:id/bet

Place a bet on a market.

Request body:
```json
{
  "outcome": "yes",
  "amount_usdc": 50.00,
  "wallet_address": "0x..."
}
```

Response:
```json
{
  "success": true,
  "data": {
    "order_id": "uuid",
    "market_id": "uuid",
    "outcome": "yes",
    "amount_usdc": 50.00,
    "potential_payout": 68.49,
    "implied_probability": 0.73,
    "kelly_suggestion": {
      "recommended_fraction": 0.08,
      "recommended_amount_usdc": 40.00,
      "reasoning": "At 73% implied probability with 37% payout odds, Kelly suggests 8% of bankroll"
    },
    "arc_tx_hash": "0x...",
    "settlement": "pending",
    "message": "Bet placed. USDC held in escrow on Arc. Resolves May 20."
  }
}
```

## GET /portfolio/:wallet

All positions and resolved P&L for a wallet address.

```json
{
  "success": true,
  "data": {
    "wallet_address": "0x...",
    "summary": {
      "total_wagered_usdc": 350.00,
      "total_won_usdc": 420.00,
      "total_lost_usdc": 200.00,
      "open_exposure_usdc": 150.00,
      "net_pnl_usdc": 220.00,
      "win_rate": 0.62
    },
    "open_positions": [
      {
        "market_id": "uuid",
        "market_title": "Will CBN hold rates above 26.5%?",
        "outcome": "yes",
        "amount_usdc": 50.00,
        "current_probability": 0.73,
        "potential_payout": 68.49,
        "closes_at": "2026-05-20T14:00:00Z"
      }
    ],
    "resolved_positions": [
      {
        "market_id": "uuid",
        "market_title": "Will Nigeria CPI exceed 33% in April?",
        "outcome": "yes",
        "amount_usdc": 100.00,
        "result": "won",
        "pnl_usdc": 37.00,
        "arc_payout_tx": "0x...",
        "resolved_at": "2026-05-14T10:00:00Z"
      }
    ]
  }
}
```

## GET /markets/:id/ai-rationale

Full AI reasoning trace for a market's current probability.

```json
{
  "success": true,
  "data": {
    "market_id": "uuid",
    "market_title": "Will CBN hold rates above 26.5%?",
    "probability_yes": 0.73,
    "confidence": "high",
    "generated_at": "2026-05-17T06:00:00Z",
    "rationale": "Based on analysis of the following data points:\n\n1. CBN Governor Cardoso's speech on May 12 signalled continued commitment to monetary tightening...\n2. Nigeria's April CPI came in at 33.69% (NBS, May 15), still far above the CBN's 21.4% target...\n3. Parallel market naira weakened 2.3% in the past week, adding imported inflation pressure...\n4. Of the last 6 MPC meetings, the CBN has held or raised rates 5 times under current governor...\n\nConclusion: High probability (73%) the CBN holds rates. Primary downside risk is unexpected sharp naira appreciation or political pressure from presidency.",
    "key_factors": [
      "CPI still 12pp above CBN target",
      "Governor Cardoso hawkish rhetoric maintained",
      "Naira parallel rate under renewed pressure"
    ],
    "risk_factors": [
      "Surprise naira appreciation could justify a cut",
      "Political pressure from presidency ahead of budget season"
    ],
    "sources": [
      {
        "title": "CBN Governor Speech, May 12 2026",
        "url": "https://cbn.gov.ng/...",
        "type": "official"
      },
      {
        "title": "Nigeria CPI April 2026 — NBS Report",
        "url": "https://nigerianstat.gov.ng/...",
        "type": "official"
      },
      {
        "title": "Naira weakens at parallel market — Reuters",
        "url": "https://reuters.com/...",
        "type": "news"
      }
    ],
    "data_snapshot": {
      "nigeria_cpi_april": 33.69,
      "cbn_current_rate": 26.75,
      "naira_parallel_rate": 1642,
      "naira_official_rate": 1580
    }
  }
}
```

## POST /markets/create

Agent-triggered endpoint to propose and create new markets.
Protected by ADMIN_API_KEY.

Request body:
```json
{
  "vertical": "nigerian_macro",
  "trigger": "scheduled",
  "api_key": "ADMIN_API_KEY"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "markets_created": 2,
    "markets": [
      {
        "id": "uuid",
        "title": "Will Nigeria's May 2026 CPI exceed 34%?",
        "vertical": "nigerian_macro",
        "resolution_criteria": "Resolution YES if NBS official CPI release for May 2026 states headline inflation exceeds 34.0%.",
        "closes_at": "2026-06-15T12:00:00Z",
        "initial_probability_yes": 0.61
      }
    ]
  }
}
```
