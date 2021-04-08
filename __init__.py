# Importing required modules
import os
from flask import Flask

# Function that is used in order to create our 'app'
def create_app(test_config=None):
    '''
    sets the test_config=None when called.
    creates a variable to contain our Flask application, with the required configurations
    Configures the secret keys
    uses an if test in order to configure and load the config file to use for our app
    imports some required local files in order to register both blueprints and url rules
    '''
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    
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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Import all the blueprints and defining url rules
# -------------------------------------------------------
    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import map
    app.register_blueprint(map.bp)
    app.add_url_rule('/worldmap', endpoint='index')
    
    from . import top5
    app.register_blueprint(top5.bp)
    app.add_url_rule('/top5', endpoint='top5')

    from . import bottom5
    app.register_blueprint(bottom5.bp)
    app.add_url_rule('/bottom5', endpoint='bottom5')

    from . import scandinavian
    app.register_blueprint(scandinavian.bp)
    app.add_url_rule('/scandinavia', endpoint='scandinavia')
    
    return app