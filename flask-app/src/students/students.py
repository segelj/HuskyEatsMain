from flask import Blueprint, request, jsonify, make_response, current_app, abort
import json, decimal
from src import db
from datetime import date as dt


students = Blueprint('students', __name__)

# MA tax rate
TAX_RATE = decimal.Decimal(0.0625)
# husky eats fee rate
FEE_RATE = decimal.Decimal(0.1)
# order initial state
INIT_STATE = 'processing'

# Get all students from the DB
@students.route('/students', methods=['GET'])
def get_students():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Student')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

# Get student detail for student with particular studentID
@students.route('/students/<studentID>', methods=['GET'])
def get_student(studentID):
    select_stmt = 'SELECT * FROM Student WHERE student_id = {0}'\
        .format(studentID)
    current_app.logger.info(select_stmt)
    cursor = db.get_db().cursor()
    cursor.execute(select_stmt)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# create a new student with specified student detail
@students.route('/student', methods=['POST'])
def create_student():
    req_data = request.get_json()
    first_name = req_data['first_name']
    last_name = req_data['last_name']
    phone = req_data['phone']
    building_id = req_data['building_id']

    insert_stmt = 'INSERT INTO Student (first_name, last_name, phone, building_id) \
        VALUES ("{0}", "{1}", "{2}", {3})'.format(first_name, last_name, phone, building_id)

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    return "Success"

# update student detail for student with particular studentID
@students.route('/students/<studentID>', methods=['PUT'])
def update_student(studentID):
    req_data = request.get_json()
    first_name = req_data['first_name']
    last_name = req_data['last_name']
    phone = req_data['phone']
    building_id = req_data['building_id']

    update_stmt = 'UPDATE Student SET first_name = "{0}", last_name = "{1}", phone = "{2}", \
        building_id = {3} WHERE student_id = {4}'.format(first_name, last_name, phone, \
            building_id, studentID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"

# delete a student with particular studentID
@students.route('/students/<studentID>', methods=['DELETE'])
def delete_student(studentID):
    delete_stmt = 'DELETE FROM Student WHERE student_id = {0}'.format(studentID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"

# Get all orders
@students.route('/orders', methods=['GET'])
def get_orders():
    cursor = db.get_db().cursor()

    query = """SELECT order_id, date, status, student_id, name, first_name, last_name,
    subtotal, tip, fee, tax, driver_rating, res_rating FROM Orders
    LEFT OUTER JOIN Driver D on D.driver_id = Orders.driver_id
    LEFT OUTER JOIN Restaurant R on Orders.restaurant_id = R.restaurant_id"""

    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)

@students.route('/order', methods=['POST'])
def create_order():
    req_data = request.get_json()
    student_id = req_data['student_id']
    products = req_data['products']
    subtotal = req_data['subtotal']
    tip = req_data['tip']
    fee = req_data['fee']
    tax = req_data['tax']
    rest_id = req_data['restaurant_id']
    date = dt.today()
    
    new_order_query = f"""INSERT INTO Orders (date, subtotal, tip, fee, tax, status, student_id, restaurant_id)
    VALUES ("{date}", {subtotal}, {tip}, {fee}, {tax}, 'pending', {student_id}, {rest_id})"""

    cursor = db.get_db().cursor()
    cursor.execute(new_order_query)
    order_id = cursor.lastrowid
    for product_id in products:
        new_op_query = f"""INSERT INTO OrderProduct (order_id, product_id)
        VALUES ({order_id}, {product_id})"""
        cursor.execute(new_op_query)
    db.get_db().commit()

    return "Success"

# Get all orders placed by a specified student
@students.route('/orders/<studentID>', methods=['GET'])
def get_student_orders(studentID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Orders WHERE student_id = {0}'.format(studentID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete all orders placed by a specified student
@students.route('/orders/<studentID>', methods=['DELETE'])
def delete_student_orders(studentID):
    delete_stmt = 'DELETE FROM Orders WHERE student_id = {0}'.format(studentID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"

# Get a particular order specified by order ID
@students.route('/orders/<orderID>', methods=['GET'])
def get_order(orderID):
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT * FROM Orders WHERE order_id = {0}'.format(orderID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# update the tip amount of a particular order
@students.route('/orders/<orderID>/tip', methods=['PUT'])
def update_order_tip(orderID):
    req_data = request.get_json()
    tip = req_data['tip']
    update_stmt = 'UPDATE Orders SET tip = {0} WHERE order_id = {1}'.format(tip, orderID)

    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"

# update the restaurant rating of a particular order
@students.route('/orders/<orderID>/resRating', methods=['PUT'])
def update_order_restaurant_rating(orderID):
    req_data = request.get_json()
    stars = req_data['stars']
    
    insert_stmt = 'INSERT INTO ResRating (restaurant_id, stars) VALUES (\
        (SELECT restaurant_id FROM Orders WHERE order_id = {0}), {1})'.format(orderID, stars)
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    res_rating_id = cursor.lastrowid
    update_stmt = 'UPDATE Orders SET res_rating = {0} WHERE order_id = {1}'\
        .format(res_rating_id, orderID)
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"

# update the driver rating of a particular order
@students.route('/orders/<orderID>/driverRating', methods=['PUT'])
def update_order_driver_rating(orderID):
    req_data = request.get_json()
    stars = req_data['stars']
    
    insert_stmt = 'INSERT INTO DriverRating (driver_id, stars) VALUES (\
        (SELECT driver_id FROM Orders WHERE order_id = {0}), {1})'.format(orderID, stars)
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    driver_rating_id = cursor.lastrowid
    update_stmt = 'UPDATE Orders SET driver_rating = {0} WHERE order_id = {1}'\
        .format(driver_rating_id, orderID)
    cursor.execute(update_stmt)
    db.get_db().commit()

    return "Success"

# Delete a particular order
@students.route('/orders/<orderID>', methods=['DELETE'])
def delete_order(orderID):
    delete_stmt = 'DELETE FROM Orders WHERE order_id = {0}'.format(orderID)

    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    db.get_db().commit()

    return "Success"
