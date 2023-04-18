from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)


# Get all customers from the DB


@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Student')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


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
