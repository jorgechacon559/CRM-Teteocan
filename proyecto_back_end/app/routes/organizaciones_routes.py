from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import organizaciones_controller, usuario_controller

organizaciones_api = Blueprint('organizaciones_api', __name__)

def get_usuario_actual():
    current_user_id = get_jwt_identity()
    from app.models.usuario import Usuario
    usuario = Usuario.query.get(current_user_id)
    return usuario

# Crear organización (protegido, solo agentes autenticados)
@organizaciones_api.route('/', methods=['POST'])
@jwt_required()
def crear_organizacion():
    usuario_actual = get_usuario_actual()
    if not usuario_actual:
        return jsonify({"mensaje": "Usuario no encontrado"}), 401
    data = request.get_json()
    resultado, status_code = organizaciones_controller.crear_organizacion(data)
    return jsonify(resultado), status_code

# Listar organizaciones (protegido, solo agentes autenticados)
@organizaciones_api.route('/', methods=['GET'])
@jwt_required()
def listar_organizaciones():
    usuario_actual = get_usuario_actual()
    filtros = request.args.to_dict()
    resultado = organizaciones_controller.listar_organizaciones(filtros, usuario_actual)
    return jsonify(resultado), 200

# Obtener detalles de una organización (protegido)
@organizaciones_api.route('/<int:organizacion_id>', methods=['GET'])
@jwt_required()
def obtener_organizacion(organizacion_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = organizaciones_controller.obtener_organizacion(organizacion_id, usuario_actual)
    return jsonify(resultado), status_code

# Editar organización (protegido, solo admin o agente asignado)
@organizaciones_api.route('/<int:organizacion_id>', methods=['PUT'])
@jwt_required()
def editar_organizacion(organizacion_id):
    usuario_actual = get_usuario_actual()
    data = request.get_json()
    resultado, status_code = organizaciones_controller.editar_organizacion(organizacion_id, data, usuario_actual)
    return jsonify(resultado), status_code

# Liberar prospecto (solo admin)
@organizaciones_api.route('/<int:organizacion_id>/liberar', methods=['PUT'])
@jwt_required()
def liberar_prospecto(organizacion_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = organizaciones_controller.liberar_prospecto(organizacion_id, usuario_actual)
    return jsonify(resultado), status_code

# Reasignar prospecto (solo admin)
@organizaciones_api.route('/<int:organizacion_id>/reasignar', methods=['PUT'])
@jwt_required()
def reasignar_prospecto(organizacion_id):
    usuario_actual = get_usuario_actual()
    data = request.get_json()
    nuevo_usuario_id = data.get("nuevo_usuario_id")
    resultado, status_code = organizaciones_controller.reasignar_prospecto(organizacion_id, nuevo_usuario_id, usuario_actual)
    return jsonify(resultado), status_code

# Importar organizaciones desde Excel (puedes dejarlo público si solo admin lo usa desde backend, o protegerlo)
@organizaciones_api.route('/importar-excel', methods=['POST'])
@jwt_required()
def importar_organizaciones_excel():
    usuario_actual = get_usuario_actual()
    # Solo admin puede importar
    if usuario_actual.get("rol") != "admin":
        return jsonify({"mensaje": "No autorizado"}), 403
    if 'file' not in request.files:
        return jsonify({"mensaje": "No se envió archivo"}), 400
    file = request.files['file']
    resultado = organizaciones_controller.importar_organizaciones_excel(file)
    return jsonify(resultado), 200

# Obtener historial de asignaciones de prospectos
@organizaciones_api.route('/<int:organizacion_id>/historial-asignaciones', methods=['GET'])
@jwt_required()
def get_historial_asignaciones(organizacion_id):
    usuario_actual = get_usuario_actual()
    resultado, status_code = organizaciones_controller.historial_asignaciones(organizacion_id, usuario_actual)
    return jsonify(resultado), status_code

