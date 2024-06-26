# DATABASE SETUP

You can both use a local installation and official docker of mysql. Commands used inside (# Create database and source .sql file) will be identical. 

## Set docker mysql

NOTE: mysql is the container name here. Feel free to change pasword and name.

	docker pull mysql
	docker run --name mysql -e MYSQL_ROOT_PASSWORD=123123 -p 3306:3306 -d mysql:latest

## Import using .sql file

I added a test.sql file inside database/ directory, which is produced by the operations on Manual Import part. So, you can just use this steps to import database from that file. 

Copy file and get into mysql:

	docker cp <path-to-sql>/test.sql mysql:/home/test.sql
	docker exec -it mysql bash
	mysql -p123123
	
## Create database and source .sql file

	CREATE DATABASE import_test;
	USE import_test;
	source /home/test.sql;

## Manual Import

I created the tables according my guess of data type and set the limits to not create data clipping. Still there is no constraint, if you have any ideas feel free to add them.

### copy files

	docker cp Downloads/archive mysql:/home/

### connect to docker and open mysql cli

	docker exec -it mysql bash
	mysql -p123123

### create database and set local_infile to be able to use LOAD DATA LOCAL

	CREATE DATABASE test;
	USE test;
	SET GLOBAL local_infile=1;

### re-enter using --local-infile=1 argument to be able to use LOAD DATA LOCAL

	exit
	mysql --local-infile=1 -uroot -p123123
	USE test;
	
### create tables and load data onto them

	CREATE TABLE category(
		category_id CHAR(3),
		employee_id INT,
		category_name VARCHAR(30),
		rating VARCHAR(5),
		quantity_sold INT,
		being_manufactured INT,
		total_sold_value INT
		);
	LOAD DATA LOCAL INFILE '/home/archive/category.csv' INTO TABLE category FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	create table employee(
	employee_id int unsigned primary key,
	store_id int unsigned, 
	firstname varchar(100) NOT NULL,
	lastname varchar(100) NOT NULL, 
	dob date not null, 
	email varchar(100) not null check(email like '%@%'), 
	status varchar(10) not null, 
	salary int unsigned not null check(salary > 0), 
	city varchar(100) not null, 
	country varchar(100) not null,

	foreign key(store_id)
	references store (store_id)
	on delete set null
	on update cascade
	);
	LOAD DATA LOCAL INFILE '/home/archive/employee.csv' INTO TABLE employee FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	create table customer(
	customer_id int unsigned primary key,
	employee_id int unsigned,
	firstname varchar(100) NOT NULL,
	lastname varchar(100) NOT NULL,
	dob date not null,
	email varchar(100) not null check(email like '%@%'),
	city varchar(100) not null,
	country varchar(100) not null,

	foreign key(employee_id)
	references employee (employee_id)
	on delete set null
	on update cascade
	);
	LOAD DATA LOCAL INFILE '/home/archive/customer.csv' INTO TABLE customer FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	CREATE TABLE provider(
		provider_id INT AUTO_INCREMENT PRIMARY KEY,
		employee_id INT,
		provider_name VARCHAR(40),
		debt INT,
		email VARCHAR(40),
		city VARCHAR(30),
		country VARCHAR(60),
		FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
		);
	LOAD DATA LOCAL INFILE '/home/archive/provider.csv' INTO TABLE provider FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	CREATE TABLE product(
		product_id INT AUTO_INCREMENT,
		provider_id INT,
		category_id CHAR(3),
		product_name VARCHAR(20),
		model VARCHAR(40),
		year INT,
		color VARCHAR(20),
		km INT,
		price INT,
		PRIMARY KEY (product_id),
		FOREIGN KEY (provider_id) REFERENCES provider(provider_id) ON DELETE RESTRICT ON UPDATE CASCADE
		);
	LOAD DATA LOCAL INFILE '/home/archive/product.csv' INTO TABLE product FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	CREATE TABLE store(
		store_id INT AUTO_INCREMENT,
		employee_id INT,
		store_name VARCHAR(40),
		phone CHAR(10),
		street VARCHAR(40),
		city VARCHAR(30),
		country VARCHAR(60),
		email VARCHAR(40),
		post_code INT,
		PRIMARY KEY(store_id),
		FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
		);
	LOAD DATA LOCAL INFILE '/home/archive/store.csv' INTO TABLE store FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	CREATE TABLE orders(
		order_id INT AUTO_INCREMENT PRIMARY KEY,
		customer_id INT,
		product_id INT,
		store_id INT,
		employee_id INT,
		order_date CHAR(10),
		ship_date CHAR(10),
		required_date CHAR(10),
		order_status VARCHAR(9),
		quantity INT,
		FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY (store_id) REFERENCES store(store_id) ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
		);
	LOAD DATA LOCAL INFILE '/home/archive/order.csv' INTO TABLE orders FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	create table rise_archive(
	rise_id varchar(10) primary key,
	amount_by_percent smallint unsigned not null check(amount_by_percent > 0),
	rise_date date not null,
	rise_state char(9) not null
	);
	LOAD DATA LOCAL INFILE '/home/archive/rise_archive.csv' INTO TABLE rise_archive FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \W;

	ALTER TABLE employee ADD CONSTRAINT store_id FOREIGN KEY (store_id) REFERENCES store(store_id) ON DELETE RESTRICT ON UPDATE CASCADE;

### to export use mysqldump command

	mysqldump --databases --user=root --password test > /home/test.sql

### additional notes

Since, category is not normalized and not have constraints, products cannot have foreign key on it.
