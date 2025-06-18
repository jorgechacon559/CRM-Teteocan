from ..extensions import db

class DetalleEmpresa(db.Model):
    __tablename__ = 'detalles_empresas'

    empresa_id = db.Column(db.Integer, primary_key=True)
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.organizacion_id'), nullable=False)
    numero_empleados = db.Column(db.Integer, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    # Relación con organización (uno a uno)
    organizacion = db.relationship('Organizacion', backref=db.backref('detalle_empresa', uselist=False), lazy=True)

    def to_dict(self):
        return {
            "empresa_id": self.empresa_id,
            "organizacion_id": self.organizacion_id,
            "numero_empleados": self.numero_empleados,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }