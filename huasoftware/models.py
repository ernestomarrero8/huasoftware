from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    apellido = db.Column(db.String(64), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Huaso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    ciudad = db.Column(db.String(64), nullable=False)
    pais = db.Column(db.String(64), nullable=False)
    caballo = db.relationship('Caballo', backref='dueño', uselist=False)
    puntajes = db.relationship('Puntaje', backref='huaso', lazy=True)

class Caballo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    numero_inscripcion = db.Column(db.Integer, unique=True, nullable=False)
    huaso_id = db.Column(db.Integer, db.ForeignKey('huaso.id'), nullable=False)

class Puntaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntaje = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    huaso_id = db.Column(db.Integer, db.ForeignKey('huaso.id'), nullable=False)
