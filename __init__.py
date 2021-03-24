# Importing required modules
import os
from flask import Flask


# Function that is used in order to create our 'app'
def create_app(test_config=None):
    '''Docstring'''
    
    app = Flask(__name__, instance_relative_config=True)
    # __name__ : Telling Python to use the current python module in order to configure the required paths.
    # instance_relative_config=True : 
        # instance    : Foldername from where to load config files.
        # relative    : Path to the folder. 
        # config=True : Where python should store files that will not be commited to version control etc

    app.config.from_mapping(
        SECRET_KEY='dev'
        )
    # Secret key is used by Flask and extensions in order to keep data safe.
    # The 'dev' SHOULD be overriden with a random value when deploying!

    # Loop to veriy that our configuration has been configured.
    if test_config is None:  
        app.config.from_pyfile('config.py', silent=True)
        # Loading the configurations from config.py
    else:
        app.config.from_mapping(test_config)
        # Loading the configurations from test_config 


    # Checking if the required folders for our app exists and can be used by our app.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Remember that the os module is unnable to create these required folders if they do not exist.



    # Testing how to build a connection between a simple page and a function
# ---------------------------------------
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
# ---------------------------------------   

    # Import all the blueprints and define url rules
# -------------------------------------------------------
    from . import map
    app.register_blueprint(map.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import top5
    app.register_blueprint(top5.bp)
    app.add_url_rule('/top5', endpoint='top5')
# -------------------------------------------------------
    return app