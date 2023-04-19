SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `huskyeatsdb` ;
CREATE SCHEMA IF NOT EXISTS `huskyeatsdb` DEFAULT CHARACTER SET latin1 ;
USE `huskyeatsdb`;

-- -----------------------------------------------------
-- Table `Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Building
(
    name VARCHAR(50),
    building_id INT NOT NULL AUTO_INCREMENT,
    coordinates VARCHAR(100),
    street_name VARCHAR(100),
    zip INT,
    street_num INT,
    state VARCHAR(50),
    PRIMARY KEY (building_id)
);

-- -----------------------------------------------------
-- Table `Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Student
(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(50),
    student_id INT NOT NULL AUTO_INCREMENT,
    building_id INT,
    PRIMARY KEY (student_id),
    CONSTRAINT fk_studentbuilding
        FOREIGN KEY (building_id) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict
);

-- -----------------------------------------------------
-- Table `Driver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Driver
(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    driver_id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (driver_id)
);

-- -----------------------------------------------------
-- Table `ResCategory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ResCategory
(
    category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (category_id)
);

-- -----------------------------------------------------
-- Table `Restaurant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Restaurant
(
    name VARCHAR(100),
    open_time TIME,
    close_time TIME,
    category_id INT,
    restaurant_id INT NOT NULL AUTO_INCREMENT,
    building_id INT,
    PRIMARY KEY (restaurant_id),
    CONSTRAINT fk_categoryres
        FOREIGN KEY (category_id) REFERENCES ResCategory (category_id)
            ON UPDATE cascade ON DELETE restrict,
    CONSTRAINT fk_buildingres
        FOREIGN KEY (building_id) REFERENCES Building (building_id)
            ON UPDATE cascade ON DELETE restrict
);

-- -----------------------------------------------------
-- Table `Menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Menu
(
    name VARCHAR(100),
    menu_id INT NOT NULL AUTO_INCREMENT,
    restaurant_id INT,
    PRIMARY KEY (menu_id),
    CONSTRAINT fk_restaurantmenu
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id)
            ON UPDATE cascade ON DELETE cascade
);

-- -----------------------------------------------------
-- Table `ProductCategory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ProductCategory
(
    category_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (category_id)
);

-- -----------------------------------------------------
-- Table `Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Product
(
    name VARCHAR(100),
    product_id INT NOT NULL AUTO_INCREMENT,
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
            ON UPDATE cascade ON DELETE restrict
);

-- -----------------------------------------------------
-- Table `ResRating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS ResRating
(
    restaurant_id INT,
    rating_id INT NOT NULL AUTO_INCREMENT,
    stars INT,
    PRIMARY KEY (rating_id)
);

-- -----------------------------------------------------
-- Table `DriverRating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS DriverRating
(
    driver_id INT,
    rating_id INT NOT NULL AUTO_INCREMENT,
    stars INT,
    PRIMARY KEY (rating_id)
);

-- -----------------------------------------------------
-- Table `Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Orders
(
    subtotal DECIMAL(10,2),
    tip DECIMAL(10,2),
    fee DECIMAL(10,2),
    tax DECIMAL(10,2),
    date DATE,
    order_id INT NOT NULL AUTO_INCREMENT,
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

-- -----------------------------------------------------
-- Table `Route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Route
(
    order_id INT,
    route_id INT NOT NULL AUTO_INCREMENT,
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

-- -----------------------------------------------------
-- Table `OrderProduct`
-- -----------------------------------------------------
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