from waitress import serve
from app import app # Asegúrate que 'app' sea el nombre de tu archivo Flask

if __name__ == "__main__":
    print("Servidor iniciado en http://0.0.0.0:8080")
    # Aquí es donde le das los 2GB de RAM indirectamente permitiendo más hilos
    serve(app, host='0.0.0.0', port=8080, threads=8)