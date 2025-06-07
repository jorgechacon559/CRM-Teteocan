from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import reportes_controller, usuario_controller

reportes_api = Blueprint('reportes_api', __name__)

def get_usuario_actual():
    current_user_id = get_jwt_identity()
    usuario, _ = usuario_controller.get_data_usuario(current_user_id, None)
    return usuario

# Resumen general de organizaciones por estado
@reportes_api.route('/resumen-organizaciones', methods=['GET'])
@jwt_required()
def resumen_organizaciones():
    usuario_actual = get_usuario_actual()
    # if usuario_actual.rol != "admin":
    #     return jsonify({"mensaje": "No autorizado"}), 403
    data = reportes_controller.resumen_general()
    return jsonify(data), 200

# Organizaciones por nivel de digitalización
@reportes_api.route('/organizaciones-nivel-digital', methods=['GET'])
@jwt_required()
def organizaciones_nivel_digital():
    data = reportes_controller.organizaciones_por_nivel_digitalizacion()
    return jsonify(data), 200

# Seguimientos por usuario
@reportes_api.route('/seguimientos-por-usuario', methods=['GET'])
@jwt_required()
def seguimientos_por_usuario():
    data = reportes_controller.seguimientos_por_usuario()
    return jsonify(data), 200

# Conversiones prospecto a cliente
@reportes_api.route('/conversiones', methods=['GET'])
@jwt_required()
def conversiones():
    data = reportes_controller.conversiones_prospecto_cliente()
    return jsonify(data), 200