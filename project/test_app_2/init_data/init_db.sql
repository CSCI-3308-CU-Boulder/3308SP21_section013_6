/* Create database tables */
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  user_name VARCHAR(30) NOT NULL,
  password VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS images (
  user_id PRIMARY KEY REFERENCES users (user_id),
  image_array integer ARRAY
);