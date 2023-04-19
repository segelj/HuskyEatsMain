USE `huskyeatsdb`;

INSERT INTO Building (name, coordinates, street_name, zip, street_num, state)
VALUES
('West Village A', '47.6569,-122.3106', 'NE Campus Pkwy', 98105, 4726, 'MA'),
('Davenport A', '47.6565,-122.3097', 'NE Campus Pkwy', 98105, 3915, 'MA'),
('Kennedy Hall', '47.6597,-122.3056', 'NE 45th St', 98105, 4515, 'MA'),
('International Village', '47.6564,-122.3115', 'NE Campus Pkwy', 98105, 4245, 'MA'),
('Curry Student Center', '47.6585,-122.3069', 'NE 45th St', 98105, 4545, 'MA'),
('West Village C', '47.6561,-122.3139', 'NE Campus Pkwy', 98105, 4240, 'MA'),
('West Village G', '89.6585,-126.3069', 'NE 45th St', 98105, 4545, 'MA'),
('Marino', '49.6561,-129.3139', 'NE Campus Pkwy', 98105, 4240, 'MA');

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

INSERT INTO Driver (first_name, last_name)
VALUES
('John', 'Doe'),
('Jane', 'Doe'),
('Bob', 'Smith'),
('Alice', 'Johnson'),
('Jack', 'Lee'),
('Sarah', 'Williams'),
('David', 'Brown'),
('Emily', 'Davis'),
('Michael', 'Wilson'),
('Sophia', 'Garcia');

INSERT INTO ResCategory (name)
VALUES ('Fast Food'),
       ('Fine Dining'),
       ('Casual Dining');

INSERT INTO Restaurant (name, open_time, close_time, category_id, building_id)
VALUES
    ('McDonalds', '08:00:00', '22:00:00', 1, 2),
    ('Burger King', '08:00:00', '22:00:00', 2, 1),
    ('JP Licks', '10:00:00', '23:00:00', 3, 5),
    ('Taco Bell', '09:00:00', '21:00:00', 1, 6),
    ('Pizza Hut', '11:00:00', '22:00:00', 2, 3),
    ('Stetson East', '10:00:00', '21:00:00', 3, 4),
    ('KFC', '08:00:00', '21:00:00', 1, 2),
    ('Subway', '10:00:00', '20:00:00', 3, 2);

INSERT INTO Menu (name, restaurant_id)
VALUES
    ('Breakfast Menu', 6),
    ('Lunch Menu', 3),
    ('Dinner Menu', 8),
    ('Value Menu', 2),
    ('Burgers', 5),
    ('Drinks', 7),
    ('Dessert', 1),
    ('Appetizers', 4),
    ('Gluten Free', 2),
    ('Vegan', 8);

INSERT INTO ProductCategory (name)
VALUES ('BBQ'),
       ('Pizza'),
       ('Sandwiches'),
       ('Drinks'),
       ('Dessert');

INSERT INTO Product (name, restaurant_id, description, price, menu_id, category_id)
VALUES
    ('Cheeseburger', 2, 'A hamburger with a slice of cheese on it.', 6.99, 10, 4),
    ('Impossible Burger', 7, 'A burger made from plants', 10.99, 7, 5),
    ('Hamburger', 5, 'A round patty of ground beef', 9.99, 6, 2),
    ('Salad', 1, 'A cold dish of various mixtures of raw or cooked vegetables', 13.99, 5, 1),
    ('Pepperoni Pizza', 6, 'Large pepperoni pizza with tomato sauce and mozzarella cheese', 11.99, 2, 3),
    ('Spaghetti Bolognese', 8, 'Spaghetti with meat sauce made with ground beef, tomatoes, and herbs', 5.99, 8, 4),
    ('Green Salad', 4, 'Mixed greens with cucumber, cherry tomatoes, and balsamic vinaigrette dressing', 13.99, 1, 2),
    ('Cheese Pizza', 3, 'Plain cheese pizza', 6.99, 4, 5),
    ('Caesar Salad', 2, 'A salad consisting of romaine lettuce and croutons', 10.99, 9, 1),
    ('Ice Cream', 6, 'Its cold and yummy! Ice cream!', 12.99, 3, 3);

INSERT INTO ResRating (restaurant_id, stars)
VALUES (3, 2),
       (6, 4),
       (7, 3),
       (4, 5),
       (5, 4),
       (2, 2),
       (8, 4),
       (1, 4),
       (1, 3),
       (7, 4),
       (5, 2),
       (4, 1),
       (6, 2),
       (3, 1),
       (8, 4);

INSERT INTO DriverRating (driver_id, stars)
VALUES (1, 5),
       (2, 4),
       (3, 3),
       (4, 2),
       (5, 1);

INSERT INTO Orders (subtotal, tip, fee, tax, date, status, student_id, restaurant_id, driver_id, driver_rating, res_rating)
VALUES
(25.97, 4.90, 1.50, 2.38, '2023-04-07', 'delivered', 1, 1, 1, 3, 5),
(34.97, 5.25, 1.50, 3.23, '2023-04-07', 'cancelled', 2, 2, 2, NULL, 4),
(17.98, 3.40, 1.50, 1.08, '2023-04-06', 'delivered', 3, 3, 3, 4, NULL),
(22.97, 4.35, 1.50, 1.78, '2023-04-06', 'delivered', 4, 1, 5, NULL, NULL),
(15.99, 3.04, 1.50, 1.13, '2023-04-05', 'delivered', 5, 3, 4, NULL, 3);

INSERT INTO Route (order_id, buildingA, buildingB)
VALUES
(3, 4, 3),
(2, 6, 6),
(4, 4, 3),
(1, 3, 5),
(5, 5, 4);

INSERT INTO OrderProduct (order_id, product_id)
VALUES
(1, 5),
(3, 2),
(5,  7),
(4,  6),
(2,  6);