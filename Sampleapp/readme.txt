DATABASE SETUP


MySQL Setup:
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
sudo systemctl start mysql.service

sudo su

mysql -u root

CREATE USER ''username''@''localhost'' IDENTIFIED BY ''password'';

GRANT ALL PRIVILEGES ON . TO ''username''@''localhost'';

exit

mysql -u username -p
create database my_first_db;
exit
mysql -u username -p my_first_db > my_first_db.sql

Postgres Setup:
sudo apt install postgresql
sudo su – postgres
psql
alter user postgres password ‘<password>’
exit
sudo -u postgres createdb cavisson
locate pg_hba.conf
change in  pg_hba.conf
	local   all             postgres                                peer 
to  local   all             postgres                                 md5
sudo service postgres restart




CREATE TABLE todos (
id SERIAL PRIMARY KEY ,
task VARCHAR ( 50 ) NOT NULL,
completed BOOLEAN
);
exit
MongoDB Setup:
sudo apt install -y mongodb
sudo systemctl unmask mongodb
sudo service mongodb start

Redis Setup:
sudo apt install redis


