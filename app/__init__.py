from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.Config')

    with app.app_context():
        from . import views
        app.register_blueprint(views.bp)

    return app
