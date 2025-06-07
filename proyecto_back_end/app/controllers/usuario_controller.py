from app.models.usuario import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import jsonify

def get_all_users(usuario_actual):
    if usuario_actual.rol != 'admin':
        return {"mensaje": "No autorizado"}, 403
    usuarios = Usuario.query.all()
    list_usuario = [{
        "usuario_id": usuario.usuario_id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "baja": usuario.baja,
        "rol": usuario.rol
    } for usuario in usuarios]
    return {'success': True, 'data': list_usuario}, 200

def get_data_usuario(usuario_id, usuario_actual):
    """Un agente solo puede ver su propio perfil. Admin puede ver cualquiera."""
    if usuario_actual.rol != 'admin' and usuario_actual.usuario_id != usuario_id:
        return {"mensaje": "No autorizado"}, 403
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404
    return {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "usuario_id": usuario.usuario_id,
        "rol": usuario.rol
    }, 200

def registrar_usuario(data):
    """Registro público solo para agentes."""
    usuario_existente = Usuario.query.filter_by(email=data['email']).first()
    if usuario_existente:
        return {"mensaje": "El usuario ya existe"}, 400
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    nuevo_usuario = Usuario(
        rol='agente',
        nombre=data['nombre'],
        apellido=data['apellido'],
        email=data['email'],
        password=hashed_password,
        baja=False,
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return {
        "mensaje": "Usuario registrado con éxito",
        "usuario": {
            "nombre": nuevo_usuario.nombre,
            "apellido": nuevo_usuario.apellido,
            "email": nuevo_usuario.email,
            "usuario_id": nuevo_usuario.usuario_id
        }
    }, 201

def login_usuario(data):
    """Login de usuario, retorna JWT si es correcto."""
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return {"mensaje": "Faltan credenciales"}, 400
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and not usuario.baja and check_password_hash(usuario.password, password):
        access_token = create_access_token(identity=usuario.usuario_id)
        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario_id": usuario.usuario_id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "rol": usuario.rol,
            "email": usuario.email,
            "access_token": access_token
        }, 200
    else:
        return {"mensaje": "Credenciales incorrectas"}, 401

def editar_usuario(usuario_id, data, usuario_actual):
    """Editar perfil propio (nombre, apellido, email, password). Admin puede editar cualquiera."""
    if usuario_actual.rol != 'admin' and usuario_actual.usuario_id != usuario_id:
        return {"mensaje": "No autorizado"}, 403
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404
    for campo in ['nombre', 'apellido', 'email']:
        if campo in data:
            setattr(usuario, campo, data[campo])
    if 'password' in data and data['password']:
        usuario.password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    db.session.commit()
    return {"mensaje": "Usuario actualizado correctamente"}, 200

def desactivar_usuario(usuario_id, usuario_actual):
    """Solo admin puede dar de baja a un usuario."""
    if usuario_actual.rol != 'admin':
        return {"mensaje": "No autorizado"}, 403
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"mensaje": "Usuario no encontrado"}, 404
    usuario.baja = True
    db.session.commit()
    return {"mensaje": "Usuario dado de baja correctamente"}, 200