from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Huaso, Caballo, Puntaje, User
from . import db
from datetime import datetime
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['Usuario']
        password = request.form['Contraseña']
        user = User.query.filter_by(correo=correo).first()
        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('main.login'))
        return redirect(url_for('main.registro'))
    return render_template('login.html')

@main_bp.route('/nuevo-usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('main.nuevo_usuario'))
        
        if User.query.filter_by(correo=correo).first() is not None:
            flash('El correo ya está registrado')
            return redirect(url_for('main.nuevo_usuario'))
        
        new_user = User(nombre=nombre, apellido=apellido, correo=correo)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cuenta creada exitosamente')
        return redirect(url_for('main.login'))
    return render_template('nuevo_usuario.html')

@main_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['nacimiento']
        ciudad = request.form['ciudad']
        pais = request.form['pais']
        nombrecaballo = request.form['nombrecaballo']
        inscripcion = request.form['inscripcion']

        # Convertir fecha_nacimiento a formato YYYY-MM-DD
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            flash('Formato de fecha incorrecto. Use DD-MM-YYYY')
            return redirect(url_for('main.registro'))

        nuevo_huaso = Huaso(rut=rut, nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento, ciudad=ciudad, pais=pais)
        db.session.add(nuevo_huaso)
        db.session.commit()
        
        nuevo_caballo = Caballo(nombre=nombrecaballo, numero_inscripcion=inscripcion, huaso_id=nuevo_huaso.id)
        db.session.add(nuevo_caballo)
        db.session.commit()
        
        flash('Registro guardado exitosamente')
        return redirect(url_for('main.registro'))
    return render_template('registro.html')

@main_bp.route('/puntaje', methods=['GET', 'POST'])
def puntaje():
    if request.method == 'POST':
        idhuaso = request.form['idhuaso']
        ptje1 = request.form['ptje1']
        ptje2 = request.form['ptje2']
        ptje3 = request.form['ptje3']
        
        huaso = Huaso.query.filter_by(id=idhuaso).first()
        if huaso is None:
            flash('Participante no encontrado')
            return redirect(url_for('main.puntaje'))
        
        nuevo_puntaje = Puntaje(puntaje=ptje1, fecha=datetime.utcnow(), huaso_id=huaso.id)
        db.session.add(nuevo_puntaje)
        
        nuevo_puntaje = Puntaje(puntaje=ptje2, fecha=datetime.utcnow(), huaso_id=huaso.id)
        db.session.add(nuevo_puntaje)
        
        nuevo_puntaje = Puntaje(puntaje=ptje3, fecha=datetime.utcnow(), huaso_id=huaso.id)
        db.session.add(nuevo_puntaje)
        
        db.session.commit()
        flash('Puntajes guardados exitosamente')
        return redirect(url_for('main.puntaje'))
    
    puntajes = Puntaje.query.all()
    return render_template('puntaje.html', puntajes=puntajes)

@main_bp.route('/tablaposicion')
def tablaposicion():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    subquery = db.session.query(
        Huaso.id.label('huaso_id'), Huaso.nombre, Huaso.apellidos,
        Caballo.nombre.label('nombrecaballo'),
        func.sum(Puntaje.puntaje).label('total_puntaje')
    ).join(Caballo, Huaso.id == Caballo.huaso_id).join(Puntaje, Huaso.id == Puntaje.huaso_id)\
     .group_by(Huaso.id, Caballo.nombre).subquery()
    
    query = db.session.query(
        subquery.c.nombre, subquery.c.apellidos, subquery.c.nombrecaballo, subquery.c.total_puntaje
    ).order_by(subquery.c.total_puntaje.desc())
    
    huasos = query.paginate(page=page, per_page=per_page, error_out=False)
    
    next_url = url_for('main.tablaposicion', page=huasos.next_num, per_page=per_page) if huasos.has_next else None
    prev_url = url_for('main.tablaposicion', page=huasos.prev_num, per_page=per_page) if huasos.has_prev else None
    
    return render_template('tablaposicion.html', huasos=huasos.items, next_url=next_url, prev_url=prev_url, total_pages=huasos.pages)

@main_bp.route('/fechas', methods=['GET', 'POST'])
def fechas():
    if request.method == 'POST':
        fecha = request.form['fecha']
        ubicacion = request.form['ubicacion']
        # Aquí iría la lógica para guardar las fechas
        flash('Fecha guardada exitosamente')
        return redirect(url_for('main.fechas'))
    return render_template('fechas.html')
