from flask import Flask
from flask_cors import CORS


def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

    if testing:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    from . import routes
    app.register_blueprint(routes.bp)

    return app
