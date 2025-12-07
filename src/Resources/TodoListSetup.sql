-- SQLite schema for Todo List application
PRAGMA foreign_keys = ON;

-- Projects table: stores categories/projects for todo items
CREATE TABLE IF NOT EXISTS Project (
	project_id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL
);

-- Todo_Item table: tasks belonging (optionally) to a project
CREATE TABLE IF NOT EXISTS Todo_Item (
	todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
	completed TEXT NOT NULL CHECK (completed IN ('yes', 'no')),
	project_id INTEGER,
	created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

-- Helpful indexes for queries
CREATE INDEX IF NOT EXISTS idx_todo_project ON Todo_Item(project_id);
CREATE INDEX IF NOT EXISTS idx_todo_priority ON Todo_Item(priority);

-- Seed data (optional) - a small sample to get started
INSERT OR IGNORE INTO Project (project_id, title) VALUES (1, 'General');
INSERT OR IGNORE INTO Project (project_id, title) VALUES (2, 'Work');
INSERT OR IGNORE INTO Project (project_id, title) VALUES (3, 'Personal');

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id, created_at)
	VALUES (1, 'Buy groceries', 'Milk, eggs, bread', 3, 'no', 3, datetime('now'));

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id, created_at)
	VALUES (2, 'Finish report', 'Complete the monthly financial report', 5, 'no', 2, datetime('now'));

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id, created_at)
	VALUES (3, 'Call plumber', 'Fix kitchen sink leak', 4, 'yes', 1, datetime('now'));

-- End of schema
