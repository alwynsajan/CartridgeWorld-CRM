-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS CWdb;
USE CWdb;

-- Step 2: Create customerData Table
CREATE TABLE IF NOT EXISTS customerData (
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    customerType VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    state VARCHAR(50),
    postcode VARCHAR(10),
    ABN VARCHAR(20)
);

-- Step 3: Create productData Table
CREATE TABLE IF NOT EXISTS productData (
    productID INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    name VARCHAR(50) NOT NULL,
    productType VARCHAR(50),
    price DECIMAL(10,2)
);

-- Step 4: Create PerdaySale Table
CREATE TABLE IF NOT EXISTS PerdaySale (
    date DATE NOT NULL PRIMARY KEY,
    sales DECIMAL(10,2) NOT NULL
);

-- Step 5: Create salesData Table
CREATE TABLE IF NOT EXISTS salesData (
    saleID INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    customerID INT,
    productList VARCHAR(500),
    paymentType VARCHAR(50) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES customerData(customerID) ON DELETE SET NULL
);

-- Step 6: Verify Tables
SHOW TABLES;
