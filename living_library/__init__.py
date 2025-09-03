import os

from flask import Flask

from living_library.data import database

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'living-library.sqlite')
    )

    # sqlalchemy configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///living-library.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    database.db.init_app(app)
    
    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initializing connection to db
    from . import auth, book
    database.init_db(app)

    # registering blueprint endpoints
    app.register_blueprint(auth.bp)

    app.register_blueprint(book.bp)
    app.add_url_rule('/shelves', endpoint='index')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    return app
