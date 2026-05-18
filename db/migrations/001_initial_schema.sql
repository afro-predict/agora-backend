-- ============================================================
-- MARKETS
-- ============================================================
CREATE TABLE markets (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title                 TEXT NOT NULL,
    description           TEXT NOT NULL,
    vertical              TEXT NOT NULL CHECK (vertical IN (
                              'nigerian_macro',
                              'african_macro',
                              'global_macro'
                          )),
    resolution_criteria   TEXT NOT NULL,
    source_of_truth       TEXT NOT NULL,
    probability_yes       FLOAT NOT NULL DEFAULT 0.5,
    probability_updated_at TIMESTAMPTZ,
    status                TEXT NOT NULL DEFAULT 'open' CHECK (status IN (
                              'open',
                              'closed',
                              'resolved',
                              'voided'
                          )),
    outcome               TEXT CHECK (outcome IN ('yes', 'no', NULL)),
    closes_at             TIMESTAMPTZ NOT NULL,
    resolved_at           TIMESTAMPTZ,
    created_by            TEXT DEFAULT 'agent',
    total_yes_usdc        FLOAT DEFAULT 0,
    total_no_usdc         FLOAT DEFAULT 0,
    created_at            TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ORDERS (individual bets)
-- ============================================================
CREATE TABLE orders (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    market_id         UUID REFERENCES markets(id) ON DELETE CASCADE,
    wallet_address    TEXT NOT NULL,
    outcome           TEXT NOT NULL CHECK (outcome IN ('yes', 'no')),
    amount_usdc       FLOAT NOT NULL CHECK (amount_usdc > 0),
    kelly_suggestion  FLOAT,
    potential_payout  FLOAT,
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN (
                          'active',
                          'won',
                          'lost',
                          'refunded'
                      )),
    arc_tx_hash       TEXT,
    circle_wallet_id  TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- POSITIONS (aggregated per wallet per market)
-- ============================================================
CREATE TABLE positions (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_address   TEXT NOT NULL,
    market_id        UUID REFERENCES markets(id) ON DELETE CASCADE,
    outcome          TEXT NOT NULL CHECK (outcome IN ('yes', 'no')),
    total_usdc       FLOAT NOT NULL DEFAULT 0,
    avg_probability  FLOAT,
    pnl_usdc         FLOAT DEFAULT 0,
    status           TEXT NOT NULL DEFAULT 'open' CHECK (status IN (
                         'open', 'won', 'lost', 'refunded'
                     )),
    UNIQUE(wallet_address, market_id, outcome)
);

-- ============================================================
-- RESOLUTIONS (agent resolution log)
-- ============================================================
CREATE TABLE resolutions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    market_id           UUID REFERENCES markets(id) ON DELETE CASCADE,
    outcome             TEXT NOT NULL CHECK (outcome IN ('yes', 'no')),
    source_url          TEXT NOT NULL,
    agent_reasoning     TEXT NOT NULL,
    confidence          TEXT CHECK (confidence IN ('high', 'medium', 'low')),
    resolved_by         TEXT DEFAULT 'agent',
    arc_resolution_tx   TEXT,
    resolved_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- AI RATIONALE (probability scoring log)
-- ============================================================
CREATE TABLE ai_rationale (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    market_id       UUID REFERENCES markets(id) ON DELETE CASCADE,
    probability_yes FLOAT NOT NULL,
    rationale       TEXT NOT NULL,
    confidence      TEXT CHECK (confidence IN ('high', 'medium', 'low')),
    sources         JSONB,
    data_snapshot   JSONB,
    generated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- WALLETS (Circle wallet registry)
-- ============================================================
CREATE TABLE wallets (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_address    TEXT UNIQUE NOT NULL,
    circle_wallet_id  TEXT UNIQUE,
    usdc_balance      FLOAT DEFAULT 0,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_markets_status     ON markets(status);
CREATE INDEX idx_markets_vertical   ON markets(vertical);
CREATE INDEX idx_markets_closes_at  ON markets(closes_at);
CREATE INDEX idx_orders_wallet      ON orders(wallet_address);
CREATE INDEX idx_orders_market      ON orders(market_id);
CREATE INDEX idx_positions_wallet   ON positions(wallet_address);
CREATE INDEX idx_rationale_market   ON ai_rationale(market_id);
