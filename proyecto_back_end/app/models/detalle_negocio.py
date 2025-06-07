from ..extensions import db

class DetalleNegocio(db.Model):
    __tablename__ = 'detalles_negocios'

    negocio_id = db.Column(db.Integer, primary_key=True)
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.organizacion_id'), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=True)
    horario_cierre = db.Column(db.Time, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    # Relación con organización (uno a uno)
    organizacion = db.relationship('Organizacion', backref=db.backref('detalle_negocio', uselist=False), lazy=True)

    def to_dict(self):
        return {
            "negocio_id": self.negocio_id,
            "organizacion_id": self.organizacion_id,
            "horario_apertura": self.horario_apertura.strftime("%H:%M") if self.horario_apertura else None,
            "horario_cierre": self.horario_cierre.strftime("%H:%M") if self.horario_cierre else None,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }