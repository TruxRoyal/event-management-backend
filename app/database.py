from app import db, create_app

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Base de datos creada correctamente')