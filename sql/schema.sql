--Schema for tables creation

CREATE TABLE city (
  city_id SERIAL PRIMARY KEY,
  city_name VARCHAR(255) NOT NULL,
  city_postal_code VARCHAR(20),
  population INTEGER,
  last_modification_year TIMESTAMP
);

CREATE TABLE category (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(255) NOT NULL
);

CREATE TABLE app_user (
  user_id SERIAL PRIMARY KEY,
  user_name VARCHAR(255) NOT NULL,
  creation_date DATE DEFAULT CURRENT_DATE,
  long NUMERIC(9,6),
  lat NUMERIC(9,6)
);

CREATE TABLE poi (
  poi_id SERIAL PRIMARY KEY,
  category_id INTEGER REFERENCES category(category_id),
  city_id INTEGER REFERENCES city(city_id),
  poi_name VARCHAR(255) NOT NULL,
  long NUMERIC(9,6),
  lat NUMERIC(9,6),
  last_modification_date TIMESTAMP,
  description TEXT,
  web_address TEXT,
  postal_address TEXT
);

CREATE TABLE category_poi (
  category_poi_id SERIAL PRIMARY KEY,
  poi_id INTEGER REFERENCES poi(poi_id),
  category_id INTEGER REFERENCES category(category_id)
);

CREATE TABLE user_profile (
  user_profile_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES app_user(user_id),
  category_id INTEGER REFERENCES category(category_id),
  max_distance INTEGER,
  transport_mean VARCHAR(50)
);

CREATE TABLE category_user_profile (
  category_user_profile_id SERIAL PRIMARY KEY,
  category_id INTEGER REFERENCES category(category_id),
  user_profile_id INTEGER REFERENCES user_profile(user_profile_id)
);

CREATE TABLE itinerary_step (
  itinerary_step_id SERIAL PRIMARY KEY,
  itinerary_step VARCHAR(255) NOT NULL
);

CREATE TABLE itinerary (
  user_id INTEGER REFERENCES app_user(user_id),
  poi_id INTEGER REFERENCES poi(poi_id),
  itinerary_step_id INTEGER REFERENCES itinerary_step(itinerary_step_id),
  duration INTEGER,
  --start_poi_id INTEGER REFERENCES poi(poi_id),
  --end_poi_id INTEGER REFERENCES poi(poi_id),
  step_order INTEGER,
  PRIMARY KEY (user_id, poi_id, itinerary_step_id)
);
