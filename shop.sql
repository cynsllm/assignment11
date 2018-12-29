CREATE database shop;

USE shop;

CREATE TABLE categories (
id INT NOT NULL AUTO_INCREMENT,
category VARCHAR(30) NOT NULL,
PRIMARY KEY (id));

DROP TABLE products;
CREATE TABLE products (
id INT NOT NULL AUTO_INCREMENT,
title VARCHAR(30) NOT NULL,
description TEXT NOT NULL,
price VARCHAR(30) NOT NULL,
img_url TEXT NOT NULL,
category_id INT NOT NULL,
favorite BOOL,
PRIMARY KEY (id),
FOREIGN KEY (category_id)
REFERENCES categories(id)
ON UPDATE CASCADE
ON DELETE RESTRICT);







