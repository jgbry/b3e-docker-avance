CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  favorite_insult VARCHAR(255) NOT NULL
);

INSERT INTO users (name, favorite_insult) VALUES
('Alice', 'mergeur fou'),
('Bob', 'cowboy du CSS'),
('Charlie', 'copieur StackOverflow'),
('Diana', 'oubliateur de tests'),
('Eve', 'push master sur main');