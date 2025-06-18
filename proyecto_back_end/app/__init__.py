from flask import Flask
from .config import Config
from .extensions import init_extensions
from flask_cors import CORS

# Importa los blueprints reales y actualizados
from .routes import (
    usuarios_api,
    organizaciones_api,
    seguimientos_api,
    reportes_api
)

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    app.config.from_object(Config)
    app.config['JSON_SORT_KEYS'] = False

    init_extensions(app)

    # Registra cada blueprint con su prefijo correspondiente
    app.register_blueprint(usuarios_api, url_prefix='/api/usuarios')
    app.register_blueprint(organizaciones_api, url_prefix='/api/organizaciones')
    app.register_blueprint(seguimientos_api, url_prefix='/api/seguimientos')
    app.register_blueprint(reportes_api, url_prefix='/api/reportes')

    print(app.url_map)
    return app