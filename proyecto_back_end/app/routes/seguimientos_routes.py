from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import seguimientos_controller, usuario_controller

seguimientos_api = Blueprint('seguimientos_api', __name__)

def get_usuario_actual():
    current_user_id = get_jwt_identity()
    from app.models.usuario import Usuario
    usuario = Usuario.query.get(current_user_id)
    return usuario

# Registrar un seguimiento (primer contacto o seguimiento posterior)
@seguimientos_api.route('/registrar', methods=['POST'])
@jwt_required()
def registrar_seguimiento():
    usuario_actual = get_usuario_actual()
    data = request.get_json()
    resultado, status_code = seguimientos_controller.registrar_seguimiento(data, usuario_actual)
    return jsonify(resultado), status_code

# Listar seguimientos de una organización (historial)
@seguimientos_api.route('/organizacion/<int:organizacion_id>', methods=['GET'])
@jwt_required()
def listar_seguimientos_por_organizacion(organizacion_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = seguimientos_controller.listar_seguimientos_por_organizacion(organizacion_id, usuario_actual)
    return jsonify(resultado), status_code

# Listar seguimientos de un usuario (historial personal o para dashboard)
@seguimientos_api.route('/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def listar_seguimientos_por_usuario(usuario_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = seguimientos_controller.listar_seguimientos_por_usuario(usuario_id, usuario_actual)
    return jsonify(resultado), status_code

# Editar seguimiento (solo admin, historial normalmente inmutable)
@seguimientos_api.route('/<int:seguimiento_id>', methods=['PUT'])
@jwt_required()
def editar_seguimiento(seguimiento_id):
    usuario_actual = get_usuario_actual()
    data = request.get_json()
    resultado, status_code = seguimientos_controller.editar_seguimiento(seguimiento_id, data, usuario_actual)
    return jsonify(resultado), status_code

# Eliminar seguimiento (solo admin, historial normalmente inmutable)
@seguimientos_api.route('/<int:seguimiento_id>', methods=['DELETE'])
@jwt_required()
def eliminar_seguimiento(seguimiento_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = seguimientos_controller.eliminar_seguimiento(seguimiento_id, usuario_actual)
    return jsonify(resultado), status_code

# Listar seguimientos generales (dashboard, admin)
@seguimientos_api.route('/', methods=['GET'])
@jwt_required()
def listar_seguimientos_generales():
    usuario_actual = get_usuario_actual()
    filtros = request.args.to_dict()
    resultado, status_code = seguimientos_controller.listar_seguimientos_generales(filtros, usuario_actual)
    return jsonify(resultado), status_code