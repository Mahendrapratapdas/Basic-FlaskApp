<!-- Title -->
<h1 align="center">Flask Application with Multiple Databases</h1>

<!-- Description -->
<p align="center">A versatile Flask Application for testing MySQL, PostgreSQL, MongoDB, and Redis databases, along with HTTP Callouts and Exception Handling.</p>

<!-- Table of Contents -->
## Table of Contents
- [Python Setup](#python-setup)
- [Database Setup](#database-setup)
  - [MySQL Setup](#mysql-setup)
  - [Postgres Setup](#postgres-setup)
  - [MongoDB Setup](#mongodb-setup)
  - [Redis Setup](#redis-setup)

<!-- Python Setup -->
## Python Setup

Install the required Python packages by running the following command:

```bash


pip install -r requirements.txt


```
# Database Setup
### MySQL Setup
```bash
# Install MySQL Server
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
sudo systemctl start mysql.service

# Access MySQL
sudo su
mysql -u root

# Create a MySQL user and grant privileges
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON.TO 'username'@'localhost';
exit

# Create a MySQL database
mysql -u username -p
create database my_first_db;
exit

# Export the database schema
mysql -u username -p my_first_db > my_first_db.sql
```
### Postgres Setup
```bash
# Install PostgreSQL
sudo apt install postgresql
sudo su – postgres
psql

# Set a password for the postgres user
alter user postgres password '<password>';
exit

# Create a PostgreSQL database
sudo -u postgres createdb cavisson

Locate pg_hba.conf
# Modify pg_hba.conf for authentication
# Change 'peer' to 'md5' in the file
# From: local   all             postgres                                peer
# To:   local   all             postgres                                md5
sudo service postgres restart

# Access the PostgreSQL database
psql -U postgres -d cavisson

# Create a table 'todos' in the database
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    task VARCHAR(50) NOT NULL,
    completed BOOLEAN
);
exit
```
### MongoDB Setup
```bash
# Install MongoDB
sudo apt install -y mongodb
sudo systemctl unmask mongodb
sudo service mongodb start
```
### Redis Setup
```bash
# Install Redis
sudo apt install redis
```
