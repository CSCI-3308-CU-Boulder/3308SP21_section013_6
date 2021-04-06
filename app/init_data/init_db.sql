/* Create database tables */
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
    user_name VARCHAR(30) NOT NULL PRIMARY KEY,
    password VARCHAR(30) NOT NULL,
    email VARCHAR(30)
);

DROP TABLE IF EXISTS images CASCADE;
CREATE TABLE IF NOT EXISTS images (
  image_id VARCHAR(30) NOT NULL PRIMARY KEY,
  user_name  VARCHAR(30) NOT NULL,
  image_matrix INT[]
 );

INSERT INTO users(user_name, password, email)
VALUES ('testuser', '1234', 'you@me.com');

INSERT INTO images(image_id, user_name, image_matrix)
VALUES ('12345', 'testuser', ARRAY [1,0,1,0]);