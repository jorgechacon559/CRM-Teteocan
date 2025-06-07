from ..extensions import db

class Organizacion(db.Model):
    __tablename__ = 'organizaciones'

    organizacion_id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('empresa', 'negocio_local'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    email_contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    codigo_postal = db.Column(db.String(10), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    ubicacion = db.Column(db.String(150), nullable=True)
    sector = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
    prospecto_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=True, comment='Agente asignado')
    nivel_digitalizacion = db.Column(db.Integer, nullable=False, default=0)
    estado_organizacion = db.Column(db.Enum('prospecto', 'cliente', 'descartado'), nullable=False, default='prospecto')

    # Relaciones
    seguimientos = db.relationship('Seguimiento', backref='organizacion_ref', lazy=True)
    asignaciones = db.relationship('AsignacionProspecto', backref='organizacion', lazy=True)

    def to_dict(self):
        return {
            "organizacion_id": self.organizacion_id,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "email_contacto": self.email_contacto,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "codigo_postal": self.codigo_postal,
            "ciudad": self.ciudad,
            "ubicacion": self.ubicacion,
            "sector": self.sector,
            "categoria": self.categoria,
            "notas": self.notas,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "prospecto_id": self.prospecto_id,
            "nivel_digitalizacion": self.nivel_digitalizacion,
            "estado_organizacion": self.estado_organizacion
        }