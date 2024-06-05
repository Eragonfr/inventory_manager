DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS item_edition;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS item_usage;
DROP TABLE IF EXISTS item_usage_history;
DROP TABLE IF EXISTS project_member;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	is_admin INTEGER NOT NULL DEFAULT FALSE
);

CREATE TABLE item (
	id INTEGER PRIMARY KEY,
	name STRING NOT NULL,
	total_count INTEGER NULL
);

CREATE TABLE item_edition (
	item_id INTEGER NOT NULL,
	by_user INTEGER NOT NULL,
	date INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
	comment TEXT NULL,
	FOREIGN KEY (item_id) REFERENCES item(id),
	FOREIGN KEY (by_user) REFERENCES user(id),
	PRIMARY KEY (item_id, by_user, date)
);

CREATE TABLE project (
	id INTEGER PRIMARY KEY,
	name STRING NOT NULL
);

CREATE TABLE item_usage (
	item_id INTEGER NOT NULL,
	project_id INTEGER NOT NULL,
	count INTEGER,
	date INTEGER NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (item_id) REFERENCES item(id),
	FOREIGN KEY (project_id) REFERENCES project(id),
	PRIMARY KEY (item_id, project_id)
);

CREATE TABLE project_member (
	user_id INTEGER NOT NULL,
	project_id INTEGER NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (project_id) REFERENCES project(id),
	PRIMARY KEY (user_id, project_id)
);
