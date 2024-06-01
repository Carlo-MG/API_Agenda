from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = '12345'
    app.config['JWT_SECRET_KEY'] = '12345'
    
    db.init_app(app)
    jwt.init_app(app)

    # Importar blueprints dentro de la función para evitar importaciones circulares
    from src.Auth import auth as auth_blueprint
    from src.Routers import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
