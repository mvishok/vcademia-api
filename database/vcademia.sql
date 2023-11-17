-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS vcademia;

-- Connect to the database
\c vcademia;

-- Create the 'sessions' table
CREATE TABLE sessions (
    key serial PRIMARY KEY,
    un varchar(255),
    pw varchar(255)
);