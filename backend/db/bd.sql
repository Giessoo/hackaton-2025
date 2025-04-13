-- Таблица teams
CREATE TABLE teams (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  status INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  phone VARCHAR(255),
  password VARCHAR(255) NOT NULL,
  token VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица tasks
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  task_type SMALLINT,
  address VARCHAR(255),
  device_type VARCHAR(255),
  device_num INT,
  status SMALLINT,
  photo VARCHAR(255),
  team_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- Таблица user_teams
CREATE TABLE user_teams (
  id SERIAL PRIMARY KEY,
  team_id INT,
  user_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Триггер для автоматического обновления поля updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Применяем триггер для обновления времени
CREATE TRIGGER update_task_timestamp
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_user_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_team_timestamp
BEFORE UPDATE ON teams
FOR EACH ROW
EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_user_teams_timestamp
BEFORE UPDATE ON user_teams
FOR EACH ROW
EXECUTE PROCEDURE update_timestamp();