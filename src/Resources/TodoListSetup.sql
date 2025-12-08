-- TODO Remove before submission
DROP TABLE IF EXISTS Todo_Item;
DROP TABLE IF EXISTS Project;

-- SQLite schema for Todo List application
PRAGMA foreign_keys = ON;

-- Projects table: stores categories/projects for todo items
-- It is not good practice to have ON DELETE CASCADE on non-PRIMARY KEY fields, so it has been removed to avoid syntax errors.
CREATE TABLE IF NOT EXISTS Project (
	project_id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL UNIQUE
);

-- Todo_Item table: tasks belonging (optionally) to a project
CREATE TABLE IF NOT EXISTS Todo_Item (
	todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT NOT NULL,
	priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
	completed TEXT NOT NULL CHECK (completed IN ('yes', 'no')),
	project_id INTEGER NOT NULL,
	title TEXT NOT NULL,
	FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
	FOREIGN KEY (title) REFERENCES Project(title) ON DELETE CASCADE
);

-- Helpful indexes for queries
CREATE INDEX IF NOT EXISTS idx_todo_project ON Todo_Item(project_id);
CREATE INDEX IF NOT EXISTS idx_todo_priority ON Todo_Item(priority);

-- Seed data (optional) - a small sample to get started
INSERT OR IGNORE INTO Project (project_id, title) VALUES (1, 'General');
INSERT OR IGNORE INTO Project (project_id, title) VALUES (2, 'Work');
INSERT OR IGNORE INTO Project (project_id, title) VALUES (3, 'Personal');

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id)
	VALUES (1, 'General', 'Get milk, eggs, bread from grocery store', 3, 'no', 1);

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id)
	VALUES (2, 'Work', 'Complete the monthly financial report', 5, 'no', 2);

INSERT OR IGNORE INTO Todo_Item (todo_id, title, description, priority, completed, project_id)
	VALUES (3, 'Personal', 'Fix kitchen sink leak', 4, 'yes', 3);

-- End of schema
