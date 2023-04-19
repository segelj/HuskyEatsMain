# Some set up for the application

from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that we will use in other parts of the API
db = MySQL()


def create_app():
    app = Flask(__name__)

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'

    # these are for the DB object to be able to connect to MySQL.
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = open(
        '/secrets/db_root_password.txt').readline()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    # Change this to your DB name
    app.config['MYSQL_DATABASE_DB'] = 'huskyeatsdb'

    # Initialize the database object with the settings above.
    db.init_app(app)

    # Add a default route
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the husky eats app</h1>"

    # Import the various routes
    from src.students.students import students
    from src.restaurants.restaurants import restaurants
    from src.buildings.buildings import buildings

    # Register the routes that we just imported so they can be properly handled
    app.register_blueprint(students,   url_prefix='/s')
    app.register_blueprint(restaurants,    url_prefix='/r')
    app.register_blueprint(buildings, url_prefix='/b')

    return app
