CREATE TABLE IF NOT EXISTS "users" (
	"sub"	BLOB NOT NULL UNIQUE,
	"key_hash"	BLOB NOT NULL,
	"paste_index"	BLOB,
	PRIMARY KEY("sub")
);