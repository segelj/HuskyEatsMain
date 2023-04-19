CREATE DATABASE IF NOT EXISTS huskyeatsdb;

SHOW DATABASES;

USE huskyeatsdb;


CREATE TABLE IF NOT EXISTS Building
(
    name VARCHAR(50),
    building_id INT AUTO_INCREMENT,
    coordinates VARCHAR(100),
    street_name VARCHAR(100),
    zip INT,
    street_num INT,
    state VARCHAR(50),
    PRIMARY KEY (building_id)
);

INSERT INTO Building (name, building_id, coordinates, street_name, zip, street_num, state)
VALUES
('West Village A', 1, '47.6569,-122.3106', 'NE Campus Pkwy', 98105, 4726, 'MA'),
('Davenport A', 2, '47.6565,-122.3097', 'NE Campus Pkwy', 98105, 3915, 'MA'),
('Kennedy Hall', 3, '47.6597,-122.3056', 'NE 45th St', 98105, 4515, 'MA'),
('International Village', 4, '47.6564,-122.3115', 'NE Campus Pkwy', 98105, 4245, 'MA'),
('Curry Student Center', 5, '47.6585,-122.3069', 'NE 45th St', 98105, 4545, 'MA'),
('West Village C', 6, '47.6561,-122.3139', 'NE Campus Pkwy', 98105, 4240, 'MA'),
('West Village G', 7, '89.6585,-126.3069', 'NE 45th St', 98105, 4545, 'MA'),
('Marino', 8, '49.6561,-129.3139', 'NE Campus Pkwy', 98105, 4240, 'MA');

-- 8 records

CREATE TABLE IF NOT EXISTS Driver
(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    driver_id INT AUTO_INCREMENT,
    PRIMARY KEY (driver_id)
);

INSERT INTO Driver (first_name, last_name, driver_id)
VALUES
('John', 'Doe', 1),
('Jane', 'Doe', 2),
('Bob', 'Smith', 3),
('Alice', 'Johnson', 4),
('Jack', 'Lee', 5),
('Sarah', 'Williams', 6),
('David', 'Brown', 7),
('Emily', 'Davis', 8),
('Michael', 'Wilson', 9),
('Sophia', 'Garcia', 10);
--10 records

CREATE TABLE IF NOT EXISTS Student
(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(50),
    student_id INT AUTO_INCREMENT,
    building_id INT,
    PRIMARY KEY (student_id),
    CONSTRAINT fk_studentbuilding
        FOREIGN KEY (building_id) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict
);

INSERT INTO Student (first_name, last_name, phone, building_id)
VALUES
('Prince', 'Ransbury', '785-633-7476', 1),
('Oliver', 'Johnson', '206-555-5678', 1),
('Sophia', 'Brown', '206-555-9012', 6),
('William', 'Davis', '206-555-3456', 3),
('Isabella', 'Miller', '206-555-7890', 5),
('Liam', 'Wilson', '206-555-2345', 4),
('Jeffery', 'Spiegel', '206-555-1234', 3),
('John', 'Stevens', '206-555-1234', 4),
('Mary', 'Davenport', '206-555-1234', 6),
('Isaac', 'Smith', '206-555-1234', 5);

CREATE TABLE IF NOT EXISTS ResCategory
(
    category_id INT,
    name VARCHAR(50),
    PRIMARY KEY (category_id)
);

INSERT INTO ResCategory (category_id, name)
VALUES (1, 'Fast Food'),
       (2, 'Fine Dining'),
       (3, 'Casual Dining');

CREATE TABLE IF NOT EXISTS Restaurant
(
    name VARCHAR(100),
    open_time TIME,
    close_time TIME,
    category_id INT,
    restaurant_id INT AUTO_INCREMENT,
    building_id INT,
    PRIMARY KEY (restaurant_id),
    CONSTRAINT fk_categoryres
        FOREIGN KEY (category_id) REFERENCES ResCategory (category_id)
            ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT fk_buildingres
        FOREIGN KEY (building_id) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict
);

INSERT INTO Restaurant (name, open_time, close_time, category_id, restaurant_id, building_id)
VALUES
    ('McDonalds', '08:00:00', '22:00:00', 1, 1, 2),
    ('Burger King', '08:00:00', '22:00:00', 2, 2, 1),
    ('JP Licks', '10:00:00', '23:00:00', 3, 3, 5),
    ('Taco Bell', '09:00:00', '21:00:00', 1, 4, 6),
    ('Pizza Hut', '11:00:00', '22:00:00', 2, 5, 3),
    ('Stetson East', '10:00:00', '21:00:00', 3, 6, 4),
    ('KFC', '08:00:00', '21:00:00', 1, 7, 2),
    ('Subway', '10:00:00', '20:00:00', 3, 8, 2);

-- 8 records


CREATE TABLE IF NOT EXISTS Menu
(
    name VARCHAR(100),
    menu_id INT AUTO_INCREMENT,
    restaurant_id INT,
    PRIMARY KEY (menu_id),
    CONSTRAINT fk_restaurantmenu
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id)
            ON UPDATE cascade ON DELETE cascade
);

INSERT INTO Menu (name, menu_id, restaurant_id)
VALUES
    ('Breakfast Menu', 1, 6),
    ('Lunch Menu', 2, 3),
    ('Dinner Menu', 3, 8),
    ('Value Menu', 4, 2),
    ('Burgers', 5, 5),
    ('Drinks', 6, 7),
    ('Dessert', 7, 1),
    ('Appetizers', 8, 4),
    ('Gluten Free', 9, 2),
    ('Vegan', 10, 8);

-- 10 records

CREATE TABLE IF NOT EXISTS ProductCategory
(
    category_id INT,
    name VARCHAR(50),
    PRIMARY KEY (category_id)
);

INSERT INTO ProductCategory (category_id, name)
VALUES (1, 'BBQ'),
       (2, 'Pizza'),
       (3, 'Sandwiches'),
       (4, 'Drinks'),
       (5, 'Dessert');

CREATE TABLE IF NOT EXISTS Product
(
    name VARCHAR(100),
    product_id INT AUTO_INCREMENT,
    restaurant_id INT,
    description VARCHAR(500),
    price DECIMAL(10,2),
    menu_id INT,
    category_id INT,
    PRIMARY KEY (product_id),
    CONSTRAINT fk_productrestaurant
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_productmenu
        FOREIGN KEY (menu_id) REFERENCES Menu (menu_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_productcategory
        FOREIGN KEY (category_id) REFERENCES ProductCategory (category_id)
            ON UPDATE cascade ON DELETE cascade
);

INSERT INTO Product (name, product_id, restaurant_id, description, price, menu_id, category_id)
VALUES
    ('Cheeseburger', 1, 2, 'A hamburger with a slice of cheese on it.', 6.99, 10, 4),
    ('Impossible Burger', 2, 7, 'A burger made from plants', 10.99, 7, 5),
    ('Hamburger', 3, 5, 'A round patty of ground beef', 9.99, 6, 2),
    ('Salad', 4, 1, 'A cold dish of various mixtures of raw or cooked vegetables', 13.99, 5, 1),
    ('Pepperoni Pizza', 5, 6, 'Large pepperoni pizza with tomato sauce and mozzarella cheese', 11.99, 2, 3),
    ('Spaghetti Bolognese', 6, 8, 'Spaghetti with meat sauce made with ground beef, tomatoes, and herbs', 5.99, 8, 4),
    ('Green Salad', 7, 4, 'Mixed greens with cucumber, cherry tomatoes, and balsamic vinaigrette dressing', 13.99, 1, 2),
    ('Cheese Pizza', 8, 3, 'Plain cheese pizza', 6.99, 4, 5),
    ('Caesar Salad', 9, 2, 'A salad consisting of romaine lettuce and croutons', 10.99, 9, 1),
    ('Ice Cream', 10, 6, 'Its cold and yummy! Ice cream!', 12.99, 3, 3);

-- 10 entries

CREATE TABLE IF NOT EXISTS ResRating
(
    restaurant_id INT,
    rating_id INT,
    stars INT,
    PRIMARY KEY (rating_id)
);

INSERT INTO ResRating (restaurant_id, rating_id, stars)
VALUES (3, 1, 2),
       (6, 2, 4),
       (7, 3, 3),
       (4, 4, 5),
       (5, 5, 4),
       (2, 6, 2),
       (8, 7, 4),
       (1, 8, 4),
       (1, 9, 3),
       (7, 10,4),
       (5, 11,2),
       (4, 12,1),
       (6, 13,2),
       (3, 14,1),
       (8, 15,4);

CREATE TABLE IF NOT EXISTS DriverRating
(
    driver_id INT,
    rating_id INT,
    stars INT,
    PRIMARY KEY (rating_id)
);

INSERT INTO DriverRating (driver_id, rating_id, stars)
VALUES (1, 1, 5),
       (2, 2, 4),
       (3, 3, 3),
       (4, 4, 2),
       (5, 5, 1);

CREATE TABLE IF NOT EXISTS Orders
(
    subtotal DECIMAL(10,2),
    tip DECIMAL(10,2),
    fee DECIMAL(10,2),
    tax DECIMAL(10,2),
    date DATE,
    order_id INT AUTO_INCREMENT,
    status VARCHAR(100),
    student_id INT,
    restaurant_id INT,
    driver_id INT,
    driver_rating INT,
    res_rating INT,
    PRIMARY KEY (order_id),
    CONSTRAINT fk_orderstudent
        FOREIGN KEY (student_id) REFERENCES Student (student_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_orderrestaurant
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_orderdriver
        FOREIGN KEY (driver_id) REFERENCES Driver (driver_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_orderresrating
        FOREIGN KEY (res_rating) REFERENCES ResRating (rating_id)
            ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT fk_orderdrivrating
        FOREIGN KEY (driver_rating) REFERENCES DriverRating (rating_id)
            ON UPDATE cascade ON DELETE restrict
);

INSERT INTO Orders (subtotal, tip, fee, tax, date, order_id, status, student_id, restaurant_id, driver_id, driver_rating, res_rating)
VALUES
(25.97, 4.90, 1.50, 2.38, '2023-04-07', 1, 'delivered', 1, 1, 1, 3, 5),
(34.97, 5.25, 1.50, 3.23, '2023-04-07', 2, 'cancelled', 2, 2, 2, NULL, 4),
(17.98, 3.40, 1.50, 1.08, '2023-04-06', 3, 'delivered', 3, 3, 3, 4, NULL),
(22.97, 4.35, 1.50, 1.78, '2023-04-06', 4, 'delivered', 4, 1, 5, NULL, NULL),
(15.99, 3.04, 1.50, 1.13, '2023-04-05', 5, 'delivered', 5, 3, 4, NULL, 3);

CREATE TABLE IF NOT EXISTS Route
(
    order_id INT,
    route_id INT,
    buildingA INT,
    buildingB INT,
    PRIMARY KEY (route_id),
    CONSTRAINT fk_routedriver
        FOREIGN KEY (order_id) REFERENCES Orders (order_id)
            ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT fk_routebuildinga
        FOREIGN KEY (buildingA) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT fk_routebuildingb
        FOREIGN KEY (buildingB) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict
);

INSERT INTO Route (order_id, route_id, buildingA, buildingB)
VALUES
(3, 6, 4, 3),
(2, 7, 6, 6),
(4, 9, 4, 3),
(1, 10,3, 5),
(5, 11,5, 4);

CREATE TABLE IF NOT EXISTS OrderProduct
(
    order_id INT,
    product_id INT,
    CONSTRAINT fk_orderorder
        FOREIGN KEY (order_id) REFERENCES Orders (order_id)
            ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_orderproduct
        FOREIGN KEY (product_id) REFERENCES Product (product_id)
            ON UPDATE cascade ON DELETE cascade
);

INSERT INTO OrderProduct (order_id, product_id)
VALUES
(1, 5),
(3, 2),
(5,  7),
(4,  6),
(2,  6);
