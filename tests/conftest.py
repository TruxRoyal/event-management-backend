import pytest
from app import create_app, db
from app.models.event import Event  # Importa tus modelos si los necesitas

@pytest.fixture(scope="module")
def app():
    """Fixture para crear una instancia de la aplicación Flask con configuración de pruebas."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Usar base de datos en memoria
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Establecer el contexto de la aplicación
    with app.app_context():
        db.create_all()  # Crear todas las tablas
        yield app  # Proporcionar la aplicación para las pruebas
        db.drop_all()  # Eliminar todas las tablas al finalizar las pruebas

@pytest.fixture(scope="module")
def client(app):
    """Fixture para proporcionar un cliente de pruebas."""
    return app.test_client()

@pytest.fixture(scope="function")
def init_db(app):
    """Fixture para inicializar la base de datos antes de cada prueba."""
    with app.app_context():
        db.create_all()  # Crear todas las tablas
        yield db  # Proporcionar la base de datos para la prueba
        db.session.remove()  # Limpiar la sesión
        db.drop_all()  # Eliminar todas las tablas después de la prueba