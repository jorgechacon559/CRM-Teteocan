from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..controllers import usuario_controller
from flask_cors import CORS

usuarios_api = Blueprint('usuarios_api', __name__)
CORS(usuarios_api, origins=["http://localhost:5173"], supports_credentials=True)

@usuarios_api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    resultado, status_code = usuario_controller.login_usuario(data)
    if status_code == 200:
        usuario_id = resultado.get("usuario_id")
        access_token = create_access_token(identity=str(usuario_id))
        refresh_token = create_refresh_token(identity=str(usuario_id))
        return jsonify({
            "mensaje": resultado["mensaje"],
            "access_token": access_token,
            "refresh_token": refresh_token,
            "usuario_id": usuario_id,
            "nombre": resultado.get("nombre"),
            "apellido": resultado.get("apellido"),
            "rol": resultado.get("rol"),
            "email": resultado.get("email")
        }), 200
    else:
        return jsonify(resultado), status_code

@usuarios_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=str(current_user))
    return jsonify(access_token=new_access_token), 200

@usuarios_api.route('/registrar', methods=['POST'])
def register_user():
    data = request.get_json()
    resultado, status_code = usuario_controller.registrar_usuario(data)
    return jsonify(resultado), status_code

@usuarios_api.route('/usuarios', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    # Obtén el usuario actual desde la base de datos
    from app.models.usuario import Usuario
    usuario_actual = Usuario.query.get(current_user_id)
    if not usuario_actual or usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403
    usuarios, status_code = usuario_controller.get_all_users(usuario_actual)
    return jsonify(usuarios), status_code

@usuarios_api.route('/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_data_usuario(usuario_id):
    current_user_id = get_jwt_identity()
    usuario_actual, _ = usuario_controller.get_data_usuario(current_user_id, None)
    usuario, status_code = usuario_controller.get_data_usuario(usuario_id, usuario_actual)
    return jsonify(usuario), status_code

@usuarios_api.route('/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def editar_usuario(usuario_id):
    current_user_id = get_jwt_identity()
    usuario_actual, _ = usuario_controller.get_data_usuario(current_user_id, None)
    data = request.get_json()
    resultado, status_code = usuario_controller.editar_usuario(usuario_id, data, usuario_actual)
    return jsonify(resultado), status_code

@usuarios_api.route('/<int:usuario_id>/baja', methods=['PUT', 'OPTIONS'])
@jwt_required(optional=True)
def baja_usuario(usuario_id):
    if request.method == 'OPTIONS':
        return jsonify({'ok': True}), 200  

    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"error": "No autenticado"}), 401

    from app.models.usuario import Usuario
    usuario_actual = Usuario.query.get(current_user_id)
    if not usuario_actual or usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403

    resultado, status_code = usuario_controller.desactivar_usuario(usuario_id, usuario_actual)
    return jsonify(resultado), status_code

@usuarios_api.route('/<int:usuario_id>/hacer-admin', methods=['PUT', 'OPTIONS'])
@jwt_required(optional=True)
def hacer_admin(usuario_id):
    if request.method == 'OPTIONS':
        return jsonify({'ok': True}), 200

    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({"error": "No autenticado"}), 401

    from app.models.usuario import Usuario
    usuario_actual = Usuario.query.get(current_user_id)
    if not usuario_actual:
        return jsonify({"error": "Usuario actual no encontrado"}), 404
    if usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403
    if int(current_user_id) == int(usuario_id):
        return jsonify({"error": "No puedes ascenderte a ti mismo"}), 400

    user_obj = Usuario.query.get(usuario_id)
    if not user_obj:
        return jsonify({"error": "Usuario no encontrado"}), 404
    if user_obj.rol == "admin":
        return jsonify({"msg": "El usuario ya es admin"}), 200
    user_obj.rol = "admin"
    from app.extensions import db
    db.session.commit()
    return jsonify({"msg": "Usuario ascendido a admin"}), 200