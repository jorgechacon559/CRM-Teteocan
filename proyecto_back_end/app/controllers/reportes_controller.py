from app.extensions import db
from app.models.organizacion import Organizacion
from app.models.seguimiento import Seguimiento
from app.models.usuario import Usuario
from sqlalchemy import func

def resumen_general():
    """Resumen de organizaciones por estado (prospecto, cliente, descartado)"""
    resultado = (
        db.session.query(
            Organizacion.estado_organizacion,
            func.count(Organizacion.organizacion_id)
        )
        .group_by(Organizacion.estado_organizacion)
        .all()
    )
    return {estado: cantidad for estado, cantidad in resultado}

def organizaciones_por_nivel_digitalizacion():
    """Cantidad de organizaciones por nivel de digitalización"""
    resultado = (
        db.session.query(
            Organizacion.nivel_digitalizacion,
            func.count(Organizacion.organizacion_id)
        )
        .group_by(Organizacion.nivel_digitalizacion)
        .all()
    )
    return {nivel: cantidad for nivel, cantidad in resultado}

def seguimientos_por_usuario():
    """Cantidad de seguimientos realizados por cada usuario"""
    resultado = (
        db.session.query(
            Usuario.nombre,
            Usuario.apellido,
            func.count(Seguimiento.seguimiento_id)
        )
        .join(Seguimiento, Seguimiento.usuario_id == Usuario.usuario_id)
        .group_by(Usuario.usuario_id)
        .all()
    )
    return [
        {"usuario": f"{nombre} {apellido}", "seguimientos": cantidad}
        for nombre, apellido, cantidad in resultado
    ]

def conversiones_prospecto_cliente():
    """Cantidad de prospectos convertidos a clientes"""
    total_prospectos = db.session.query(Organizacion).filter_by(estado_organizacion='prospecto').count()
    total_clientes = db.session.query(Organizacion).filter_by(estado_organizacion='cliente').count()
    return {
        "prospectos": total_prospectos,
        "clientes": total_clientes,
        "tasa_conversion": (total_clientes / total_prospectos * 100) if total_prospectos else 0
    }