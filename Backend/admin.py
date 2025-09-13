from app import db, Usuario, app

with app.app_context():
    db.create_all()

    admin = Usuario(username="admin")
    admin.set_password("12345")
    db.session.add(admin)
    db.session.commit()

    print("Usuário admin criado")