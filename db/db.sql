CREATE TABLE sessions (
  id serial,
  name VARCHAR(32),
  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE bots (
  id serial,
  session_id BIGINT,
  n_games BIGINT
)

CREATE TABLE layers (
  id serial,
  bot_id BIGINT,
  weights text,
  biases text
)


-- reset
TRUNCATE TABLE sessions;
TRUNCATE TABLE bots;
TRUNCATE TABLE layers;
