CREATE TABLE workflow (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  name TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT FALSE,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE workflow_node (
  id BIGSERIAL PRIMARY KEY,
  workflow_id BIGINT NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
  node_type TEXT NOT NULL CHECK (node_type IN ('trigger','reaction','condition')),
  service TEXT NOT NULL,
  action TEXT NOT NULL,
  params JSONB NOT NULL DEFAULT '{}'::jsonb,
  position JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX workflow_node_params_gin ON workflow_node USING GIN (params);
CREATE TABLE workflow_edge (
  id BIGSERIAL PRIMARY KEY,
  workflow_id BIGINT NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
  source_id BIGINT NOT NULL REFERENCES workflow_node(id) ON DELETE CASCADE,
  target_id BIGINT NOT NULL REFERENCES workflow_node(id) ON DELETE CASCADE,
  branch BOOLEAN NULL
);
CREATE TABLE processed_event (
  id BIGSERIAL PRIMARY KEY,
  workflow_id BIGINT NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
  event_id TEXT NOT NULL,
  processed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (workflow_id, event_id)
);
CREATE TABLE execution (
  id BIGSERIAL PRIMARY KEY,
  workflow_id BIGINT NOT NULL REFERENCES workflow(id) ON DELETE CASCADE,
  status TEXT NOT NULL,
  input_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- A2: indexed JSONB query example
-- SELECT id FROM workflow_node WHERE params @> '{"channel":"alerts"}'::jsonb;
-- A3: event idempotency is enforced by UNIQUE(workflow_id,event_id).
