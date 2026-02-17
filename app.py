import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN SEGURA ---
# Leemos las credenciales desde el entorno, no desde el código directamente
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS DE BASE DE DATOS ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    retos = db.relationship('RegistroReto', backref='autor', lazy=True)

class RegistroReto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, default=db.func.current_date())
    reto_nombre = db.Column(db.String(100), nullable=False)
    completado = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('fecha', 'reto_nombre', 'user_id', name='_fecha_reto_user_uc'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
@login_required
def index():
    hoy = datetime.now().date()
    filas_hoy = RegistroReto.query.filter_by(fecha=hoy, user_id=current_user.id).all()
    
    total_hoy = db.session.query(db.func.sum(RegistroReto.completado)).filter_by(
        fecha=hoy, user_id=current_user.id).scalar() or 0

    registros_semana = db.session.query(
        RegistroReto.fecha, db.func.sum(RegistroReto.completado).label('suma_dia')
    ).filter(RegistroReto.user_id == current_user.id).group_by(
        RegistroReto.fecha).order_by(RegistroReto.fecha.desc()).limit(7).all()

    total_semanal = sum(r.suma_dia for r in registros_semana)
    num_dias = len(registros_semana)

    proyeccion = (total_semanal / num_dias * 7) if num_dias > 0 else 0
    if proyeccion >= 54: msj, color = "camino a una SEMANA PERFECTA 🏆", "text-info"
    elif proyeccion > 45: msj, color = "ritmo de SEMANA BUENA 👍", "text-success"
    elif proyeccion > 30: msj, color = "ritmo de SEMANA REGULAR 😐", "text-warning"
    else: msj, color = "al ritmo actual, será una SEMANA PÉSIMA 💀", "text-danger"

    return render_template('index.html', 
                           hoy=hoy, filas_hoy=filas_hoy, total_hoy=total_hoy, 
                           registros_semana=registros_semana, total_semanal=total_semanal,
                           msj_ritmo=msj, color_ritmo=color)

@app.route('/check', methods=['POST'])
@login_required
def check():
    fecha_str = request.form.get('fecha_reg')
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    reto = request.form.get('reto').strip()
    estado = int(request.form.get('estado'))

    registro = RegistroReto.query.filter_by(fecha=fecha, reto_nombre=reto, user_id=current_user.id).first()
    if registro:
        registro.completado = estado
    else:
        nuevo_registro = RegistroReto(fecha=fecha, reto_nombre=reto, completado=estado, user_id=current_user.id)
        db.session.add(nuevo_registro)
    
    db.session.commit()
    return redirect(url_for('index'))

# --- RUTAS DE LOGIN, REGISTRO Y LOGOUT ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('username')
        passw = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        nuevo_usuario = User(username=user, password=passw)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("✅ Conexión establecida y tablas verificadas en Supabase.")
        except Exception as e:
            print(f"❌ Error crítico de conexión: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)