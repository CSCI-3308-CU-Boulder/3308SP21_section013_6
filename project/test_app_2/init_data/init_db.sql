/* Create database tables */
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  user_name VARCHAR(30) NOT NULL,
  password VARCHAR(30) NOT NULL
);

DROP TABLE IF EXISTS images CASCADE;
CREATE TABLE IF NOT EXISTS images (
  user_id PRIMARY KEY REFERENCES users (user_id),
  image_array INT[]
 );

INSERT INTO users(user_name, password)
VALUES ('testuser', 'pass');