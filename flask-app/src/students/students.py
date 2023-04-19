from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


students = Blueprint('students', __name__)


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
    select_stmt = 'SELECT * FROM Student WHERE student_id = {0}'.format(studentID)
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

    insert_stmt = 'INSERT INTO Student (first_name, last_name, phone, building_id) VALUES ("'
    insert_stmt += first_name + '", "' + last_name + \
        '", "' + phone + '", ' + str(building_id) + ')'

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

    update_stmt = 'UPDATE Student SET first_name = "' + first_name + '", last_name = "'\
        + last_name + '", phone = "' + phone + '", building_id = ' + str(building_id)\
            + ' WHERE student_id = ' + str(studentID)

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

# # Get all orders placed by a specified customer
# @customers.route('/orders/<custID>', methods=['GET'])
# def get_customer_orders(custID):
#     cursor = db.get_db().cursor()
#     cursor.execute(
#         'select * from orders where customer_id = {0}'.format(custID))
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response

# # Delete all orders placed by a specified customer
# @customers.route('/orders/<custID>', methods=['DELETE'])
# def delete_customer_orders(custID):
#     delete_stmt = 'DELETE FROM orders WHERE customer_id = {0}'.format(custID)

#     cursor = db.get_db().cursor()
#     cursor.execute(delete_stmt)
#     db.get_db().commit()

#     return "Success"

# # Get a particular order placed by a specified customer
# @customers.route('/orders/<custID>/<orderID>', methods=['GET'])
# def get_customer_order(custID, orderID):
#     cursor = db.get_db().cursor()
#     cursor.execute(
#         'select * from orders where customer_id = {0} and order_id = {1}'.format(custID, orderID))
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response

# # Create a new order placed by a specified customer
# @customers.route('/order/<custID>', methods=['POST'])
# def create_customer_order(custID):
#     req_data = request.get_json()
#     products = req_data['products']
#     subtotal = req_data['subtotal']
#     tip = req_data['tip']
#     fee = req_data['fee']
#     tax = req_data['tax']
#     date = req_data['date']
#     status = req_data['status']
#     rest_id = req_data['restaurant_id']

#     insert_stmt = 'INSERT INTO orders (subtotal, tip, fee, tax, date, status, customer_id, restaurant_id) VALUES ('
#     insert_stmt += str(subtotal) + ', ' + str(tip) + ', ' + str(fee) + ', ' + \
#         str(tax) + '", "' + date + '", "' + status + \
#         '", ' + str(custID) + ', ' + str(rest_id) + ')'

#     cursor = db.get_db().cursor()
#     cursor.execute(insert_stmt)
#     order_id = cursor.lastrowid
#     for product_id in products:
#         insert_stmt = 'INSERT INTO OrderProduct (order_id, product_id) VALUES ('
#         insert_stmt += str(order_id) + ', ' + str(product_id) + ')'
#         cursor.execute(insert_stmt)
#     db.get_db().commit()

#     return "Success"

# # update the tip amount of a particular order by a specified customer
# @customers.route('/orders/<custID>/<orderID>/tip', methods=['PUT'])
# def update_customer_order_tip(custID, orderID):
#     req_data = request.get_json()
#     tip = req_data['tip']
#     update_stmt = 'UPDATE orders SET tip = {0} WHERE customer_id = {1} and order_id = {2}'.format(
#         tip, custID, orderID)

#     cursor = db.get_db().cursor()
#     cursor.execute(update_stmt)
#     db.get_db().commit()

#     return "Success"

# # update the restaurant rating of a particular order by a specified customer
# @customers.route('/orders/<custID>/<orderID>/resRating', methods=['PUT'])
# def update_customer_order_restaurant_rating(custID, orderID):
#     req_data = request.get_json()
#     resRating = req_data['res_rating']
#     update_stmt = 'UPDATE orders SET res_rating = {0} WHERE customer_id = {1} and order_id = {2}'.format(
#         resRating, custID, orderID)

#     cursor = db.get_db().cursor()
#     cursor.execute(update_stmt)
#     db.get_db().commit()

#     return "Success"

# # update the driver rating of a particular order by a specified customer
# @customers.route('/orders/<custID>/<orderID>/driverRating', methods=['PUT'])
# def update_customer_order_driver_rating(custID, orderID):
#     req_data = request.get_json()
#     driverRating = req_data['driver_rating']
#     update_stmt = 'UPDATE orders SET driver_rating = {0} WHERE customer_id = {1} and order_id = {2}'.format(
#         driverRating, custID, orderID)

#     cursor = db.get_db().cursor()
#     cursor.execute(update_stmt)
#     db.get_db().commit()

#     return "Success"

# # Delete a particular order placed by a specified customer
# @customers.route('/orders/<custID>/<orderID>', methods=['DELETE'])
# def delete_customer_order(custID, orderID):
#     delete_stmt = 'DELETE FROM orders WHERE customer_id = {0} and order_id = {1}'.format(
#         custID, orderID)

#     cursor = db.get_db().cursor()
#     cursor.execute(delete_stmt)
#     db.get_db().commit()

#     return "Success"

# # Create a restaurant rating for a particular order
# @customers.route('/order/<orderID>/resRating', methods=['POST'])
# def create_restaurant_rating(orderID):
#     req_data = request.get_json()
#     stars = req_data['stars']

#     insert_stmt = 'INSERT INTO ResRating (restaurant_id, stars) VALUES ('
#     insert_stmt += '(SELECT restaurant_id FROM orders WHERE order_id = ' + str(orderID) + '), ' + str(stars) + ')'

#     cursor = db.get_db().cursor()
#     cursor.execute(insert_stmt)
#     db.get_db().commit()

#     return "Success"

# # Create a driver rating for a particular order
# @customers.route('/order/<orderID>/driverRating', methods=['POST'])
# def create_driver_rating(orderID):
#     req_data = request.get_json()
#     stars = req_data['stars']

#     insert_stmt = 'INSERT INTO DriverRating (driver_id, stars) VALUES ('
#     insert_stmt += '(SELECT driver_id FROM orders WHERE order_id = ' + str(orderID) + '), ' + str(stars) + ')'

#     cursor = db.get_db().cursor()
#     cursor.execute(insert_stmt)
#     db.get_db().commit()

#     return "Success"

# # Create an OrderProduct entry associated with a particular order and product
# # @customers.route('/OrderProduct', methods=['POST'])
# # def create_order_product():
# #     insert_stmt = 'INSERT INTO OrderProduct (order_id, product_id) VALUES ('
# #     insert_stmt += str(orderID) + ', ' + str(productID) + ')'

# #     cursor = db.get_db().cursor()
# #     cursor.execute(insert_stmt)
# #     db.get_db().commit()

# #     return "Success"

# # Get all buildings on campus
# @customers.route('/orders', methods=['GET'])
# def get_orders():
#     cursor = db.get_db().cursor()

#     query = """SELECT order_id, date, status, student_id, name, first_name, last_name, subtotal, tip, fee, tax, driver_rating,
#     res_rating FROM Orders
#     JOIN Driver D on D.driver_id = Orders.driver_id
#     JOIN Restaurant R on Orders.restaurant_id = R.restaurant_id"""

#     cursor.execute(query)
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     return jsonify(json_data)


# # Create a building location for customer if not already exist
# @customers.route('/building', methods=['POST'])
# def create_building():
#     req_data = request.get_json()
#     name = req_data['name']
#     coord = req_data['coordinates']
#     st_name = req_data['street_name']
#     zip = req_data['zip']
#     st_num = req_data['street_num']
#     state = req_data['state']

#     insert_stmt = 'INSERT INTO building (name, coordinates, street_name, zip, street_num, state) VALUES ("'
#     insert_stmt += name + '", "' + coord + '", "' + st_name + '", ' + \
#         str(zip) + ', ' + str(st_num) + ', "' + state + '")'

#     cursor = db.get_db().cursor()
#     cursor.execute(insert_stmt)
#     db.get_db().commit()

#     return "Success"


# # Update building details for a specific building
# @customers.route('/buildings/<buildingID>', methods=['PUT'])
# def update_building(buildingID):
#     req_data = request.get_json()
#     name = req_data['name']
#     coord = req_data['coordinates']
#     st_name = req_data['street_name']
#     zip = req_data['zip']
#     st_num = req_data['street_num']
#     state = req_data['state']

#     update_stmt = 'UPDATE building SET name = {0}, coordinates = {1}, street_name = {2}, zip = {3}, street_num = {4}, state = {5} WHERE building_id = {6}'.format(
#         name, coord, st_name, zip, st_num, state, buildingID)

#     cursor = db.get_db().cursor()
#     cursor.execute(update_stmt)
#     db.get_db().commit()

#     return "Success"


# # Delete a particular building
# @customers.route('/buildings/<buildingID>', methods=['DELETE'])
# def delete_building(buildingID):
#     delete_stmt = 'DELETE FROM building WHERE building_id = {0}'.format(
#         buildingID)

#     cursor = db.get_db().cursor()
#     cursor.execute(delete_stmt)
#     db.get_db().commit()

#     return "Success"
