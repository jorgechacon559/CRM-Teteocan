from ..extensions import db

class AsignacionProspecto(db.Model):
    __tablename__ = 'asignaciones_prospectos'

    asignacion_id = db.Column(db.Integer, primary_key=True)
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.organizacion_id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False, comment='Agente asignado')
    fecha_asignacion = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "asignacion_id": self.asignacion_id,
            "organizacion_id": self.organizacion_id,
            "usuario_id": self.usuario_id,
            "fecha_asignacion": self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            "fecha_finalizacion": self.fecha_finalizacion.isoformat() if self.fecha_finalizacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }