from flask import Flask
from app.extensions import db
from user.routes.user_routes import user_bp
from tandc.routes.tc_routes import tc_bp

from user.models.user_models import User
from tandc.models.tc_models import Term_conditions

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/term_condition'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(tc_bp, url_prefix='/api/tandc')

    with app.app_context():
        db.create_all()
        print("Tables Created Successfully")

    return app