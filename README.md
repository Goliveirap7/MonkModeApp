![Login Screen]([https://ruzpvxzglurtfovcphuc.supabase.co/storage/v1/object/public/assets/login%20monkmodeapp.png](https://ruzpvxzglurtfovcphuc.supabase.co/storage/v1/object/public/assets/login%20monkmodeapp.png))

# 🧘🏽‍♂️ SHIO MONK MODE - Habit Tracker

Sistema de gestión de disciplina y registro de métricas de productividad personal. Esta aplicación permite a los usuarios monitorear sus hábitos diarios bajo la metodología "Monk Mode", centralizando la información en una arquitectura de datos en la nube.

## 🚀 Características
* **Autenticación Segura**: Sistema de login y registro con hashing de contraseñas mediante **Bcrypt**.
* **Persistencia en la Nube**: Conexión robusta a **PostgreSQL (Supabase)** utilizando Supavisor para compatibilidad con redes IPv4/IPv6.
* **Análisis de Rendimiento**: Dashboard con cálculo automático de puntos diarios y proyecciones de cumplimiento semanal.
* **Interfaz Moderna**: Diseño con estética **Glassmorphism** y fondos dinámicos servidos desde Supabase Storage.
* **Arquitectura Multiusuario**: Lógica relacional donde cada usuario gestiona su propia data de forma aislada.

## 🛠️ Stack Tecnológico
* **Backend:** Python / Flask
* **Base de Datos:** PostgreSQL (Supabase Cloud)
* **Frontend:** HTML5, CSS3 (Custom Glassmorphism), Bootstrap 5
* **Seguridad:** Flask-Login, Flask-Bcrypt, Python-Dotenv
* **DevOps:** Git para control de versiones y gestión de variables de entorno.

## 📋 Pre-requisitos
* Python 3.x
* Cuenta en Supabase (para la base de datos)

## 🔧 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Goliveirap7/MonkModeApp.git](https://github.com/Goliveirap7/MonkModeApp.git)
   cd MonkModeApp
2. Instalar dependencias:

Bash
pip install -r requirements.txt

3. Configurar variables de entorno:
Crea un archivo .env en la raíz del proyecto y añade tus credenciales:

Fragmento de código
DATABASE_URL=tu_url_de_supabase
SECRET_KEY=tu_clave_secreta_flask

4. Ejecutar la aplicación:

Bash
python app.py

Autor
Giovanni (Shio) - Desarrollo y DevOps - GitHub

📍 Lima, Perú | 2026


