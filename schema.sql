CREATE TABLE IF NOT EXISTS user_sessions (
    session_id     UUID        PRIMARY KEY,
    user_id        INT,
    start_time     TIMESTAMP,
    end_time       TIMESTAMP,
    pages_visited  TEXT[],
    device         TEXT,
    actions        TEXT[],
    pages_visited_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS product_price_history (
    product_id     UUID        PRIMARY KEY,
    price_changes  JSONB,
    current_price  NUMERIC(10, 2),
    currency       TEXT
);

CREATE TABLE IF NOT EXISTS event_logs (
    event_id   UUID PRIMARY KEY,
    event_type TEXT,
    details    TEXT
    ts         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
);

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id  UUID        PRIMARY KEY,
    user_id    INT,
    status     TEXT,
    issue_type TEXT,
    messages   TEXT[],
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_recommendations (
    recommendation_id     SERIAL      PRIMARY KEY,
    user_id               INT,
    recommended_products  TEXT[],
    last_updated          TIMESTAMP
);

CREATE TABLE IF NOT EXISTS moderation_queue (
    review_id         UUID        PRIMARY KEY,
    user_id           INT,
    product_id        INT,
    review_text       TEXT,
    rating            INT,
    moderation_status TEXT,
    flags             TEXT[],
    submitted_at      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS search_queries (
    query_id     UUID        PRIMARY KEY,
    user_id      INT,
    query_text   TEXT,
    filters      TEXT[],
    results_count INT
    ts  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
);