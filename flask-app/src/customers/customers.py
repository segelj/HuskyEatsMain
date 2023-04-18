from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)


# Get all customers from the DB


# @customers.route('/customers', methods=['GET'])
# def get_customers():
#     cursor = db.get_db().cursor()
#     cursor.execute('select first_name, last_name, phone from customers')
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response


# Get customer detail for customer with particular custID


@customers.route('/customers/<custID>', methods=['GET'])
def get_customer(custID):
    cursor = db.get_db().cursor()
    cursor.execute(
        'select * from customers where customer_id = {0}'.format(custID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# create a new customer with specified customer detail


@customers.route('/customer', methods=['POST'])
def create_customer():
    req_data = request.get_json()
    first_name = req_data['first_name']
    last_name = req_data['last_name']
    phone = req_data['phone']
    building_id = req_data['building_id']

    insert_stmt = 'INSERT INTO customers (first_name, last_name, phone, building_id) VALUES ("'
    insert_stmt += first_name + '", "' + last_name + \
        '", "' + phone + '", ' + str(building_id) + ')'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    return "Success"


# update customer detail for customer with particular custID


@customers.route('/customers/<custID>', methods=['PUT'])
def update_customer(custID):
    req_data = request.get_json()
    first_name = req_data['first_name']
    last_name = req_data['last_name']
    phone = req_data['phone']
    building_id = req_data['building_id']

    update_stmt = 'UPDATE customers SET first_name = {0}, last_name = {1}, phone = {2}, building_id = {3} WHERE customer_id = {4}'.format(
        first_name, last_name, phone, building_id, custID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"


# delete a customer with particular custID


@customers.route('/customers/<custID>', methods=['DELETE'])
def delete_customer(custID):
    delete_stmt = 'DELETE FROM customers WHERE customer_id = {0}'.format(
        custID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"


# Get all orders placed by a specified customer


@customers.route('/orders/<custID>', methods=['GET'])
def get_customer_orders(custID):
    cursor = db.get_db().cursor()
    cursor.execute(
        'select * from orders where customer_id = {0}'.format(custID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Delete all orders placed by a specified customer


@customers.route('/orders/<custID>', methods=['DELETE'])
def delete_customer_orders(custID):
    delete_stmt = 'DELETE FROM orders WHERE customer_id = {0}'.format(custID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"


# Get a particular order placed by a specified customer


@customers.route('/orders/<custID>/<orderID>', methods=['GET'])
def get_customer_order(custID, orderID):
    cursor = db.get_db().cursor()
    cursor.execute(
        'select * from orders where customer_id = {0} and order_id = {1}'.format(custID, orderID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Create a new order placed by a specified customer


@customers.route('/order/<custID>', methods=['POST'])
def create_customer_order(custID):
    req_data = request.get_json()
    subtotal = req_data['subtotal']
    tip = req_data['tip']
    fee = req_data['fee']
    tax = req_data['tax']
    date = req_data['date']
    status = req_data['status']
    rest_id = req_data['restaurant_id']

    insert_stmt = 'INSERT INTO orders (subtotal, tip, fee, tax, date, status, customer_id, restaurant_id) VALUES ('
    insert_stmt += str(subtotal) + ', ' + str(tip) + ', ' + str(fee) + ', ' + \
        str(tax) + '", "' + date + '", "' + status + \
        '", ' + str(custID) + ', ' + str(rest_id) + ')'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()

    return "Success"


# update the tip amount of a particular order by a specified customer


@customers.route('/orders/<custID>/<orderID>/<tip>', methods=['PUT'])
def update_customer_order_tip(custID, orderID, tip):
    update_stmt = 'UPDATE orders SET tip = {0} WHERE customer_id = {1} and order_id = {2}'.format(
        tip, custID, orderID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"


# update the restaurant rating of a particular order by a specified customer


@customers.route('/orders/<custID>/<orderID>/<resRating>', methods=['PUT'])
def update_customer_order_restaurant_rating(custID, orderID, resRating):
    update_stmt = 'UPDATE orders SET res_rating = {0} WHERE customer_id = {1} and order_id = {2}'.format(
        resRating, custID, orderID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"


# update the driver rating of a particular order by a specified customer


@customers.route('/orders/<custID>/<orderID>/<driverRating>', methods=['PUT'])
def update_customer_order_driver_rating(custID, orderID, driverRating):
    update_stmt = 'UPDATE orders SET driver_rating = {0} WHERE customer_id = {1} and order_id = {2}'.format(
        driverRating, custID, orderID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"



# Delete a particular order placed by a specified customer


@customers.route('/orders/<custID>/<orderID>', methods=['DELETE'])
def delete_customer_order(custID, orderID):
    delete_stmt = 'DELETE FROM orders WHERE customer_id = {0} and order_id = {1}'.format(
        custID, orderID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"


# Get all buildings on campus


@customers.route('/buildings', methods=['GET'])
def get_buildings():
    cursor = db.get_db().cursor()
    cursor.execute('select * from building')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Create a building location for customer if not already exist


@customers.route('/building', methods=['POST'])
def create_building():
    req_data = request.get_json()
    name = req_data['name']
    coord = req_data['coordinates']
    st_name = req_data['street_name']
    zip = req_data['zip']
    st_num = req_data['street_num']
    state = req_data['state']

    insert_stmt = 'INSERT INTO building (name, coordinates, street_name, zip, street_num, state) VALUES ("'
    insert_stmt += name + '", "' + coord + '", "' + st_name + '", ' + \
        str(zip) + ', ' + str(st_num) + ', "' + state + '")'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()

    return "Success"


# Get building details of a building by its id


@customers.route('/buildings/<buildingID>', methods=['GET'])
def get_building(buildingID):
    cursor = db.get_db().cursor()
    cursor.execute(
        'select * from building where building_id = {0}'.format(buildingID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Update building details of a particular building


@customers.route('/buildings/<buildingID>', methods=['PUT'])
def update_building(buildingID):
    req_data = request.get_json()
    name = req_data['name']
    coord = req_data['coordinates']
    st_name = req_data['street_name']
    zip = req_data['zip']
    st_num = req_data['street_num']
    state = req_data['state']
    
    update_stmt = 'UPDATE building SET name = {0}, coordinates = {1}, street_name = {2}, zip = {3}, street_num = {4}, state = {5} WHERE building_id = {6}'.format(
        name, coord, st_name, zip, st_num, state, buildingID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"


# Delete a particular building


@customers.route('/buildings/<buildingID>', methods=['DELETE'])
def delete_building(buildingID):
    delete_stmt = 'DELETE FROM building WHERE building_id = {0}'.format(buildingID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"