-- =========================
-- DDL (CREATE)
-- =========================
CREATE DATABASE IF NOT EXISTS bankinng;
USE bankinng;

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    account_holder VARCHAR(50),
    balance DECIMAL(10,2)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    account_id INT
);

CREATE TABLE transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    type VARCHAR(20),
    amount DECIMAL(10,2),
    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- DML (INSERT)
-- =========================
INSERT INTO accounts VALUES (1,'Shiv',10000),(2,'Amit',8000);

INSERT INTO users (username,password,account_id)
VALUES ('shiv','1234',1),('amit','1234',2);

-- =========================
-- DQL (SELECT)
-- =========================
SELECT * FROM accounts;
SELECT * FROM transactions;

-- =========================
-- TCL (TRANSACTION)
-- =========================
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;

-- =========================
-- DCL (PERMISSION)
-- =========================
CREATE USER 'appuser'@'localhost' IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE ON banking.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;