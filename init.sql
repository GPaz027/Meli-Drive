CREATE DATABASE IF NOT EXISTS drive_files;

USE drive_files;

CREATE TABLE IF NOT EXISTS public_files (id VARCHAR(255) PRIMARY KEY,name VARCHAR(255));

CREATE TABLE IF NOT EXISTS files (id VARCHAR(255) PRIMARY KEY,name VARCHAR(255),extension VARCHAR(50),owner_email VARCHAR(255),visibility BOOLEAN,last_modified DATETIME);
