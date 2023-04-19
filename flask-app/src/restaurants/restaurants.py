from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

restaurants = Blueprint('restaurants', __name__)

# Get all the restaurant names from the database
@restaurants.route('/restaurants', methods=['GET'])
def get_restaurants():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = """SELECT restaurant_id as 'id', Restaurant.name as 'name', RC.name as 'category', B.name as 'building', B.building_id, RC.category_id FROM Restaurant
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
        'select * from Restaurant where restaurant_id = {0}'.format(restaurant_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, json.dumps(json_data, default = str))))
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
    category_id = the_data['category_id']
    building_id = the_data['building_id']

    query = f"""UPDATE Restaurant 
    SET name = '{name}', category_id = '{category_id}', building_id = '{building_id}'
    WHERE restaurant_id = {restaurant_id}"""

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
    
# Deletes a menu
@restaurants.route('/restaurants/<restaurant_id>/menu/<menu_id>', methods=['DELETE'])
def delete_menu(restaurant_id):
    query = "DELETE FROM Menu WHERE menu_id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, (restaurant_id,))
    db.get_db().commit()

    return "Success"
    
# Add a product to a specified menu at a restaurant 
@restaurants.route('/restaurants/<restaurant_id>/menus/<menu_id>/product', methods=['POST'])
def add_product_to_menu(restaurant_id, menu_id):
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    product_id = the_data['product_id']
    description = the_data['description']
    price = the_data['price']
    category_id = the_data['category_id']

    query = 'INSERT INTO Product (name, product_id, restaurant_id, description, price, menu_id, category_id) VALUES ("'
    query += name + '", '
    query += str(product_id) + ', '
    query += str(restaurant_id) + ', "'
    query += description + '", '
    query += str(price) + ', '
    query += str(menu_id) + ', '
    query += str(category_id) + ')'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return "Success"

# Returns a list of all restaurants that belong to a specific category
@restaurants.route('/restaurants/<category>', methods=['GET'])
def get_restaurants_by_category(category):
    cursor = db.get_db().cursor()
    query = f"SELECT * FROM Restaurant WHERE category_id = (SELECT category_id FROM Category WHERE name = '{category}')"
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    results = cursor.fetchall()
    for row in results:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns a list of all possible categories
@restaurants.route('/restaurants/categories', methods=['GET'])
def get_restaurant_categories():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = """SELECT * FROM ResCategory"""

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