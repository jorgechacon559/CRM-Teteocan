from app.extensions import db
from app.models.seguimiento import Seguimiento
from app.models.organizacion import Organizacion
from app.models.usuario import Usuario
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

def registrar_seguimiento(data, usuario_actual):
    """
    Registrar un seguimiento (primer contacto o seguimiento posterior).
    Actualiza prospecto_id, estado_organizacion y nivel_digitalizacion automáticamente vía trigger.
    """
    organizacion_id = data.get('organizacion_id')
    tipo = data.get('tipo')  # 'prospeccion', 'seguimiento', 'cierre'
    metodo_contacto = data.get('metodo_contacto')
    comentarios = data.get('comentarios')
    valores_estado = ['prospecto', 'contactado', 'no_responde', 'interesado', 'cliente', 'descartado']
    estado = data.get('estado')
    nivel_digitalizacion = data.get('nivel_digitalizacion') 
    fecha = data.get('fecha') 

    if estado and estado not in valores_estado:
        return {'mensaje': 'Estado no válido'}, 400

    if not (organizacion_id and tipo and metodo_contacto):
        return {"mensaje": "Faltan campos obligatorios"}, 400

    org = Organizacion.query.get(organizacion_id)
    if not org:
        return {"mensaje": "Organización no encontrada"}, 404

    # Seguridad: solo admin o agente asignado puede registrar seguimiento
    if usuario_actual.rol != 'admin':
        if org.prospecto_id not in (None, usuario_actual.usuario_id):
            return {"mensaje": "No autorizado"}, 403

    seguimiento = Seguimiento(
        organizacion_id=organizacion_id,
        usuario_id=usuario_actual.usuario_id,
        tipo=tipo,
        metodo_contacto=metodo_contacto,
        comentarios=comentarios,
        estado=estado,
        nivel_digitalizacion=nivel_digitalizacion,
        fecha=datetime.strptime(fecha, "%Y-%m-%d") if fecha else datetime.now()
    )
    db.session.add(seguimiento)

    # Si la organización no tiene prospecto asignado, asígnalo aquí
    if org.prospecto_id is None:
        org.prospecto_id = usuario_actual.usuario_id

    db.session.commit()
    return {"mensaje": "Seguimiento registrado correctamente", "seguimiento_id": seguimiento.seguimiento_id}, 201

def listar_seguimientos_por_organizacion(organizacion_id, usuario_actual):
    """
    Lista el historial de seguimientos de una organización.
    Solo admin o agente asignado puede ver.
    """
    org = Organizacion.query.get(organizacion_id)
    if not org:
        return {"mensaje": "Organización no encontrada"}, 404

    if usuario_actual.rol != 'admin' and org.prospecto_id != usuario_actual.usuario_id:
        return {"mensaje": "No autorizado"}, 403

    # Mostrar todos los seguimientos, incluidos los descartados
    seguimientos = Seguimiento.query.filter_by(organizacion_id=organizacion_id).order_by(Seguimiento.fecha.desc()).all()
    resultado = [{
        "seguimiento_id": s.seguimiento_id,
        "organizacion_id": s.organizacion_id,
        "organizacion_nombre": s.organizacion.nombre if s.organizacion else "",
        "organizacion_tipo": s.organizacion.tipo if s.organizacion else "",
        "fecha": s.fecha.strftime("%Y-%m-%d %H:%M"),
        "tipo": s.tipo,
        "metodo_contacto": s.metodo_contacto,
        "comentarios": s.comentarios,
        "estado": s.estado,
        "nivel_digitalizacion": s.nivel_digitalizacion,
        "usuario_id": s.usuario_id,
        "usuario_nombre": s.usuario.nombre if s.usuario else ""
    } for s in seguimientos]
    return {"seguimientos": resultado}, 200

def listar_seguimientos_por_usuario(usuario_id, usuario_actual):
    """
    Lista todos los seguimientos realizados por un usuario (para dashboard personal o admin).
    """
    if usuario_actual.rol != 'admin' and usuario_actual.usuario_id != usuario_id:
        return {"mensaje": "No autorizado"}, 403

    # Mostrar todos los seguimientos, incluidos los descartados
    seguimientos = Seguimiento.query.filter_by(usuario_id=usuario_id).order_by(Seguimiento.fecha.desc()).all()
    resultado = [{
        "seguimiento_id": s.seguimiento_id,
        "organizacion_id": s.organizacion_id,
        "organizacion_nombre": s.organizacion.nombre if s.organizacion else "",
        "organizacion_tipo": s.organizacion.tipo if s.organizacion else "",
        "fecha": s.fecha.strftime("%Y-%m-%d %H:%M"),
        "tipo": s.tipo,
        "metodo_contacto": s.metodo_contacto,
        "comentarios": s.comentarios,
        "estado": s.estado,
        "nivel_digitalizacion": s.nivel_digitalizacion,
        "usuario_id": s.usuario_id,
        "usuario_nombre": s.usuario.nombre if s.usuario else ""
    } for s in seguimientos]
    return {"seguimientos": resultado}, 200

# Opcional: solo admin puede editar/eliminar seguimientos (normalmente el historial es inmutable)
def editar_seguimiento(seguimiento_id, data, usuario_actual):
    if usuario_actual.rol != 'admin':
        return {"mensaje": "No autorizado"}, 403
    seguimiento = Seguimiento.query.get(seguimiento_id)
    if not seguimiento:
        return {"mensaje": "Seguimiento no encontrado"}, 404
    for campo in ['tipo', 'metodo_contacto', 'comentarios', 'estado', 'nivel_digitalizacion', 'fecha']:
        if campo in data:
            if campo == 'fecha':
                setattr(seguimiento, campo, datetime.strptime(data[campo], "%Y-%m-%d"))
            else:
                setattr(seguimiento, campo, data[campo])
    db.session.commit()
    return {"mensaje": "Seguimiento actualizado correctamente"}, 200

def eliminar_seguimiento(seguimiento_id, usuario_actual):
    if usuario_actual.rol != 'admin':
        return {"mensaje": "No autorizado"}, 403
    seguimiento = Seguimiento.query.get(seguimiento_id)
    if not seguimiento:
        return {"mensaje": "Seguimiento no encontrado"}, 404
    db.session.delete(seguimiento)
    db.session.commit()
    return {"mensaje": "Seguimiento eliminado correctamente"}, 200

def listar_seguimientos_generales(filtros, usuario_actual):
    from app.models.seguimiento import Seguimiento
    from app.models.organizacion import Organizacion
    from app.models.usuario import Usuario

    query = Seguimiento.query

    # Filtros opcionales
    if 'organizacion_id' in filtros and filtros['organizacion_id']:
        query = query.filter_by(organizacion_id=filtros['organizacion_id'])
    if 'usuario_id' in filtros and filtros['usuario_id']:
        query = query.filter_by(usuario_id=filtros['usuario_id'])
    if 'estado' in filtros and filtros['estado']:
        query = query.filter_by(estado=filtros['estado'])
    if 'fecha' in filtros and filtros['fecha']:
        try:
            from datetime import datetime
            fecha = datetime.strptime(filtros['fecha'], '%Y-%m-%d')
            query = query.filter(Seguimiento.fecha >= fecha, Seguimiento.fecha < fecha.replace(hour=23, minute=59, second=59))
        except Exception:
            pass

    # Paginación
    page = int(filtros.get('page', 1))
    per_page = int(filtros.get('per_page', 50))
    pagination = query.order_by(Seguimiento.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)
    seguimientos = pagination.items

    resultado = {
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "seguimientos": [s.to_dict() for s in seguimientos]
    }
    return resultado, 200