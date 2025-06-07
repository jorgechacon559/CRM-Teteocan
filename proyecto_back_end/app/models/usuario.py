from ..extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.Enum('admin', 'agente'), nullable=False, default='agente')
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    baja = db.Column(db.Boolean, nullable=False, default=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    # Relaciones
    seguimientos = db.relationship('Seguimiento', backref='usuario_ref', lazy=True)
    asignaciones = db.relationship('AsignacionProspecto', backref='usuario', lazy=True)

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "rol": self.rol,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "baja": self.baja,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }