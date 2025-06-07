from app.extensions import db
from app.models.organizacion import Organizacion
from app.models.seguimiento import Seguimiento
from app.models.usuario import Usuario
from app.models.asignacion_prospecto import AsignacionProspecto
from app.models.detalle_empresa import DetalleEmpresa
from app.models.detalle_negocio import DetalleNegocio
from sqlalchemy import or_
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

def historial_asignaciones(organizacion_id, usuario_actual):
    """Historial de asignaciones de prospectos"""
    if not usuario_actual:
        return {"mensaje": "Usuario no autenticado"}, 401
    if usuario_actual.rol != 'admin':
        return {"mensaje": "No autorizado"}, 403
    historial = AsignacionProspecto.query.filter_by(organizacion_id=organizacion_id).order_by(AsignacionProspecto.fecha_asignacion.desc()).all()
    return [a.to_dict() for a in historial], 200

def listar_organizaciones(filtros, usuario):
    query = Organizacion.query

    # Filtro explícito por prospecto_id
    if 'prospecto_id' in filtros:
        # Acepta None, 'null', '' o 0 como "disponibles"
        if filtros['prospecto_id'] in [None, 'null', '', 0, '0']:
            query = query.filter(Organizacion.prospecto_id == None)
        else:
            query = query.filter(Organizacion.prospecto_id == int(filtros['prospecto_id']))
    elif usuario.rol == 'agente':
        # Si no se especifica, solo ve las que puede ver
        query = query.filter(
            or_(
                Organizacion.prospecto_id == None,
                Organizacion.prospecto_id == usuario.usuario_id
            )
        )

    # Filtros opcionales
    if 'tipo' in filtros:
        query = query.filter_by(tipo=filtros['tipo'])
    if 'estado_organizacion' in filtros:
        query = query.filter_by(estado_organizacion=filtros['estado_organizacion'])
    if 'nombre' in filtros:
        query = query.filter(Organizacion.nombre.ilike(f"%{filtros['nombre']}%"))
    if 'ciudad' in filtros:
        query = query.filter(Organizacion.ciudad.ilike(f"%{filtros['ciudad']}%"))
    if 'busqueda' in filtros:
        busqueda = filtros['busqueda']
        query = query.filter(
            or_(
                Organizacion.nombre.ilike(f"%{busqueda}%"),
                Organizacion.ciudad.ilike(f"%{busqueda}%"),
                Organizacion.direccion.ilike(f"%{busqueda}%")
            )
        )

    # Paginación
    page = int(filtros.get('page', 1))
    per_page = int(filtros.get('per_page', 20))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    resultado = []
    for org in pagination.items:
        detalles = None
        if org.tipo == 'empresa':
            detalles = DetalleEmpresa.query.filter_by(organizacion_id=org.organizacion_id).first()
        elif org.tipo == 'negocio_local':
            detalles = DetalleNegocio.query.filter_by(organizacion_id=org.organizacion_id).first()
        # NUEVO: obtener nombre del agente asignado si existe
        asignado_nombre = None
        if org.prospecto_id:
            usuario = Usuario.query.get(org.prospecto_id)
            if usuario:
                asignado_nombre = f"{usuario.nombre} {usuario.apellido}".strip()
        resultado.append({
            **org.to_dict(),
            "detalles": detalles.to_dict() if detalles else None,
            "asignado_nombre": asignado_nombre
        })
    return {
        "organizaciones": resultado,
        "total": pagination.total,
        "page": page,
        "per_page": per_page
    }

def editar_organizacion(organizacion_id, data, usuario):
    org = Organizacion.query.get(organizacion_id)
    if not org:
        return {"error": "Organización no encontrada"}, 404

    if usuario.rol != 'admin' and org.prospecto_id != usuario.usuario_id:
        return {"error": "No autorizado"}, 403

    # Validar que ubicación es obligatoria y texto libre
    if 'ubicacion' in data:
        if not data['ubicacion'] or not isinstance(data['ubicacion'], str):
            return {"error": "El campo 'ubicacion' es obligatorio y debe ser texto"}, 400
        org.ubicacion = data['ubicacion']
    elif org.ubicacion is None:
        return {"error": "El campo 'ubicacion' es obligatorio"}, 400

    # Validar sector/categoría según tipo
    if org.tipo == 'empresa':
        if 'sector' in data:
            if not data['sector'] or not isinstance(data['sector'], str):
                return {"error": "El campo 'sector' es obligatorio y debe ser texto"}, 400
            org.sector = data['sector']
        elif org.sector is None:
            return {"error": "El campo 'sector' es obligatorio"}, 400
    elif org.tipo == 'negocio_local':
        if 'categoria' in data:
            if not data['categoria'] or not isinstance(data['categoria'], str):
                return {"error": "El campo 'categoria' es obligatorio y debe ser texto"}, 400
            org.categoria = data['categoria']
        elif org.categoria is None:
            return {"error": "El campo 'categoria' es obligatorio"}, 400

    # Editar otros campos generales
    for campo in ['nombre', 'direccion', 'telefono', 'email_contacto', 'codigo_postal', 'ciudad', 'notas']:
        if campo in data:
            setattr(org, campo, data[campo])

    # Editar detalles según tipo
    if org.tipo == 'empresa':
        detalles = DetalleEmpresa.query.filter_by(organizacion_id=org.organizacion_id).first()
        if detalles:
            for campo in ['numero_empleados', 'sitio_web']:
                if campo in data:
                    setattr(detalles, campo, data[campo])
    elif org.tipo == 'negocio_local':
        detalles = DetalleNegocio.query.filter_by(organizacion_id=org.organizacion_id).first()
        if detalles:
            for campo in ['horario_apertura', 'horario_cierre']:
                if campo in data:
                    setattr(detalles, campo, data[campo])

    db.session.commit()
    return {"message": "Organización actualizada correctamente"}, 200

def crear_organizacion(data):
    """
    Crea una nueva organización (empresa o negocio local).
    Campos obligatorios: tipo, nombre, ciudad, ubicacion
    Campos opcionales: telefono, direccion, codigo_postal, email_contacto, notas
    Según tipo, sector (empresa) o categoría (negocio_local) es obligatorio.
    """
    # Validación de campos obligatorios generales
    tipo = data.get('tipo')
    nombre = data.get('nombre')
    ciudad = data.get('ciudad')
    ubicacion = data.get('ubicacion')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    codigo_postal = data.get('codigo_postal')
    email_contacto = data.get('email_contacto')
    notas = data.get('notas')
    estado_organizacion = data.get('estado_organizacion') or 'prospecto'

    if not tipo or tipo not in ['empresa', 'negocio_local']:
        return {"error": "El campo 'tipo' es obligatorio y debe ser 'empresa' o 'negocio_local'"}, 400
    if not nombre:
        return {"error": "El campo 'nombre' es obligatorio"}, 400
    if not ciudad:
        return {"error": "El campo 'ciudad' es obligatorio"}, 400
    if not ubicacion:
        return {"error": "El campo 'ubicacion' es obligatorio"}, 400

    # Validación de campos según tipo
    if tipo == 'empresa':
        sector = data.get('sector')
        if not sector:
            return {"error": "El campo 'sector' es obligatorio para empresas"}, 400
    else:
        sector = None

    if tipo == 'negocio_local':
        categoria = data.get('categoria')
        if not categoria:
            return {"error": "El campo 'categoria' es obligatorio para negocios locales"}, 400
    else:
        categoria = None

    # Crear la organización principal
    nueva_org = Organizacion(
        tipo=tipo,
        nombre=nombre,
        ciudad=ciudad,
        ubicacion=ubicacion,
        telefono=telefono,
        direccion=direccion,
        codigo_postal=codigo_postal,
        email_contacto=email_contacto,
        notas=notas,
        sector=sector,
        categoria=categoria,
        estado_organizacion=estado_organizacion,
    )
    db.session.add(nueva_org)
    db.session.flush()  # Para obtener el ID antes de commit

    # Crear detalles según tipo
    if tipo == 'empresa':
        numero_empleados = data.get('numero_empleados')
        sitio_web = data.get('sitio_web')
        detalle_empresa = DetalleEmpresa(
            organizacion_id=nueva_org.organizacion_id,
            numero_empleados=numero_empleados,
            sitio_web=sitio_web
        )
        db.session.add(detalle_empresa)
    elif tipo == 'negocio_local':
        horario_apertura = data.get('horario_apertura')
        horario_cierre = data.get('horario_cierre')
        detalle_negocio = DetalleNegocio(
            organizacion_id=nueva_org.organizacion_id,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre
        )
        db.session.add(detalle_negocio)

    db.session.commit()

    return {
        "mensaje": "Organización creada con éxito",
        "organizacion": nueva_org.to_dict()
    }, 201