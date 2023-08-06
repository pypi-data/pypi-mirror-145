CREATE TABLE IF NOT EXISTS "pastes" (
	"pid"	BLOB NOT NULL UNIQUE,
	"data"	BLOB NOT NULL,
	"data_hash"	BLOB NOT NULL,
	"sub"	BLOB UNIQUE,
	"expiration"	INTEGER NOT NULL,
	"encoding" TEXT,
	PRIMARY KEY("pid")
);