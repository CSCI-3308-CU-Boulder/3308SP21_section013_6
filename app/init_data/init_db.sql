/* Create database tables */
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  user_name VARCHAR(30) NOT NULL,
  password VARCHAR(30) NOT NULL
);

DROP TABLE IF EXISTS images CASCADE;
CREATE TABLE IF NOT EXISTS images (
  user_id INT PRIMARY KEY,
  image_id VARCHAR(30) NOT NULL,
  image_array INT[]
 );

INSERT INTO users(user_name, password)
VALUES ('testuser', 'pass');

INSERT INTO images(user_id, image_id, image_array)
VALUES (1, 'test' ,ARRAY [1,0,1,0]);