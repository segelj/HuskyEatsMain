from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

restaurants = Blueprint('restaurants', __name__)

# Get all the restaurant names from the database


@restaurants.route('/restaurants', methods=['GET'])
def get_restaurants():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = """SELECT restaurant_id as 'id', Restaurant.name as 'name', RC.name as 'category', B.name as 'building' FROM Restaurant
    JOIN ResCategory RC on RC.category_id = Restaurant.category_id
    JOIN Building B on B.building_id = Restaurant.building_id
    ORDER BY restaurant_id"""

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


# Return all info for a particular restaurant
@restaurants.route('/restaurants/<restaurant_id>', methods=['GET'])
def get_customer(restaurant_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        'select * from Restaurant where id = {0}'.format(restaurant_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new restaurant to the database (a new restaurant opens on campus)


@restaurants.route('/restaurant', methods=['POST'])
def add_new_restaurant():
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    open = the_data['open_time']
    close = the_data['close_time']
    category = the_data['category_id']
    restaurantid = the_data['restaurant_id']
    buildingid = the_data['building_id']

    query = 'insert into Restaurant (name, open_time, close_time, category_id, restaurant_id, building_id) values ("'
    query += name + '", "'
    query += open + '", '
    query += close + '", '
    query += category + '", '
    query += restaurantid + '", '
    query += str(buildingid) + ')'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success"

# Update info for a particular restaurant pertaining to its name, location, menu, and hours


@restaurants.route('/restaurants/<restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    open_time = the_data['open_time']
    close_time = the_data['close_time']
    category_id = the_data['category_id']
    menu = the_data['menu']
    location = the_data['location']

    query = 'UPDATE Restaurant SET name = "' + name
    + '", open_time = "' + open_time + '", close_time = "'
    + close_time + '", category_id = ' + category_id
    + ', menu = "' + menu + '", location = "'
    + location + '" WHERE restaurant_id = ' + str(restaurant_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success"

# Deletes a restaurant


@restaurants.route('/restaurants/<restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    query = "DELETE FROM Restaurant WHERE restaurant_id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, (restaurant_id,))
    db.get_db().commit()

    return "Success"


# Adds a menu to a restaurant
@restaurants.route('/restaurant/<int:restaurant_id>/menu', methods=['POST'])
def add_menu(restaurant_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    menu_id = the_data['menu_id']

    query = 'INSERT INTO Menu (name, menu_id, restaurant_id) VALUES ("'
    query += name + '", '
    query += str(menu_id) + ', '
    query += str(restaurant_id) + ')'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success"

# Gets the menus for a restaurant


@restaurants.route('/restaurant/<restaurant_id>/menu', methods=['GET'])
def get_menus(restaurant_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = f"""SELECT Menu.menu_id, Menu.name FROM Menu
    JOIN Restaurant R on R.restaurant_id = Menu.restaurant_id
    WHERE R.restaurant_id = {restaurant_id}"""

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


# Gets a list of products from the given restaurant
@restaurants.route('/restaurant/<restaurant_id>/products', methods=['GET'])
def get_all_products(restaurant_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = f"""SELECT product_id, P.name as 'name', description, price, PC.name as 'category' FROM Restaurant
    JOIN Product P on Restaurant.restaurant_id = P.restaurant_id
    JOIN ProductCategory PC on P.category_id = PC.category_id
    WHERE Restaurant.restaurant_id = {restaurant_id}"""

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


# Updates the name of a particular menu from a particular restaurant
@restaurants.route('/restaurant/<restaurant_id>/menu/<menu_id>', methods=['PUT'])
def update_menu(restaurant_id, menu_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']

    query = 'UPDATE Menu SET name = %s WHERE restaurant_id = %s AND menu_id = %s'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, (name, restaurant_id, menu_id))
    db.get_db().commit()

    return "Success"