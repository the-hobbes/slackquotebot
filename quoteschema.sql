CREATE DATABASE quotestore;

\c quotestore

CREATE TABLE quotebot_quotes (
	quote_id integer NOT NULL,
	quote_blob text NOT NULL,
);