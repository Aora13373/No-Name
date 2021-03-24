import os

from flask import Flask
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        # Only for testing..
        return 'Hello, World!'
    

    # Import all the blueprints and define url rules
    from . import map
    app.register_blueprint(map.bp)
    app.add_url_rule('/', endpoint='index')

    from . import top5
    app.register_blueprint(top5.bp)
    app.add_url_rule('/top5', endpoint='top5')

    return app