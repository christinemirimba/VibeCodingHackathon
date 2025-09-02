-- Create the database
CREATE DATABASE IF NOT EXISTS recipe_recommender;
USE recipe_recommender;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    recipes_generated INT DEFAULT 0,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the recipes table
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ingredients VARCHAR(500) NOT NULL,
    recipe_text TEXT NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the transactions table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_id VARCHAR(100) NOT NULL UNIQUE,
    amount FLOAT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
