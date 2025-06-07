from ..extensions import db

class Seguimiento(db.Model):
    __tablename__ = 'seguimientos'

    seguimiento_id = db.Column(db.Integer, primary_key=True)
    organizacion_id = db.Column(db.Integer, db.ForeignKey('organizaciones.organizacion_id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    tipo = db.Column(db.Enum('prospeccion', 'seguimiento', 'cierre'), nullable=False)
    nivel_digitalizacion = db.Column(db.Integer, nullable=True)
    estado = db.Column(
        db.Enum(
            'prospecto',
            'contactado',
            'no_responde',
            'interesado',
            'cliente',
            'descartado'
        ),
        nullable=True
    )
    comentarios = db.Column(db.Text, nullable=True)
    metodo_contacto = db.Column(
        db.Enum('whatsapp', 'email', 'llamada', 'otro'),
        nullable=True
    )
    fecha_actualizacion = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
    usuario = db.relationship('Usuario', lazy='joined', overlaps="seguimientos,usuario_ref")
    organizacion = db.relationship('Organizacion', lazy='joined', overlaps="seguimientos,organizacion_ref")

    def to_dict(self):
        return {
            "seguimiento_id": self.seguimiento_id,
            "organizacion_id": self.organizacion_id,
            "organizacion_nombre": self.organizacion.nombre if self.organizacion else "",
            "organizacion_tipo": self.organizacion.tipo if self.organizacion else "",  # <-- agrega esto
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
            "tipo": self.tipo,
            "metodo_contacto": self.metodo_contacto,
            "comentarios": self.comentarios,
            "estado": self.estado,
            "nivel_digitalizacion": self.nivel_digitalizacion,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario.nombre if self.usuario else ""
        }