BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "USER" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT(30) NOT NULL,
	"telegram_id"	INTEGER UNIQUE,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "REST_EVENT" (
	"event_id"	INTEGER NOT NULL,
	"name"	VARCHAR(128) NOT NULL,
	"counter"	INTEGER NOT NULL,
	"last_date"	TEXT(30),
	"user_id"	INTEGER,
	PRIMARY KEY("event_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "USER"("user_id") ON DELETE CASCADE
);
INSERT OR IGNORE INTO "USER" VALUES (1,'default',NULL);
COMMIT;