CREATE TABLE users (
	id SERIAL NOT NULL, 
	email VARCHAR(256) NOT NULL, 
	password_hash VARCHAR(256) NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	created_at_utc TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE incidents (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	threat_level VARCHAR(20) NOT NULL, 
	created_at_utc TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE playbooks (
	id SERIAL NOT NULL, 
	author_id INTEGER, 
	title VARCHAR(255) NOT NULL, 
	qdrant_point_id VARCHAR(64) NOT NULL, 
	created_at_utc TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES users (id) ON DELETE SET NULL, 
	UNIQUE (qdrant_point_id)
);

CREATE TABLE analysis_messages (
	id SERIAL NOT NULL, 
	incident_id INTEGER NOT NULL, 
	role message_role_enum NOT NULL, 
	content TEXT NOT NULL, 
	created_at_utc TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(incident_id) REFERENCES incidents (id) ON DELETE CASCADE
);

CREATE TABLE incident_playbooks (
	message_id INTEGER NOT NULL, 
	playbook_id INTEGER NOT NULL, 
	similarity_score NUMERIC(5, 4) NOT NULL, 
	PRIMARY KEY (message_id, playbook_id), 
	FOREIGN KEY(message_id) REFERENCES analysis_messages (id) ON DELETE CASCADE, 
	FOREIGN KEY(playbook_id) REFERENCES playbooks (id) ON DELETE CASCADE
);

CREATE TABLE llm_call_logs (
	id SERIAL NOT NULL, 
	message_id INTEGER NOT NULL, 
	provider VARCHAR(50) NOT NULL, 
	model VARCHAR(100) NOT NULL, 
	input_tokens INTEGER NOT NULL, 
	output_tokens INTEGER NOT NULL, 
	latency_ms INTEGER NOT NULL, 
	cost_usd NUMERIC(12, 6) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (message_id), 
	FOREIGN KEY(message_id) REFERENCES analysis_messages (id) ON DELETE CASCADE
);