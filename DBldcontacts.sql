
CREATE DATABASE IF NOT EXISTS osint;
GRANT USAGE ON *.* TO 'osintuser'@localhost IDENTIFIED BY 'password';
GRANT  SELECT, INSERT, UPDATE ON osint.* TO 'osintuser'@localhost;
FLUSH PRIVILEGES;
USE osint;

DROP TABLE IF EXISTS 'ldcontacts';
CREATE TABLE 'ldcontacts' (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
'name' varchar(50) NOT NULL,  
'name2' varchar(50) NOT NULL,
'surname' varchar(50) NOT NULL,
'position' varchar(500) NOT NULL,
'company' varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
