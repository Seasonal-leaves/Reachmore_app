from flask import Flask
from applications.config import Config
from applications.database import db
from applications.models import *
from flask_restful import Api
from flask_security import Security, hash_password
from applications.user_datastore import user_datastore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    api = Api(app, prefix='/api/iescp2')
    app.security = Security(app, user_datastore)


    with app.app_context():
        db.create_all()

        admin_role = app.security.datastore.find_or_create_role(name='admin')
        sponsor_role = app.security.datastore.find_or_create_role(name='sponsor')
        influencer_role = app.security.datastore.find_or_create_role(name='influencer')

        if not app.security.datastore.find_user(username = 'Ritam_admin'):
            app.security.datastore.create_user(username='Ritam_admin',
                                       email='ritam_admin@gmail.com',
                                       password=hash_password('ritam_admin'),
                                       is_approved=True,
                                       roles=[admin_role, sponsor_role])
            
        db.session.commit()
    
    return app,api

app, api = create_app()

from applications.user_api import *

api.add_resource(UserRegistration, '/register')


if __name__ == '__main__':
    app.run(debug=True)
