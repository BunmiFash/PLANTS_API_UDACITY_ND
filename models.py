import os
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = 'plantsdb'
# database_path = 'postgresql://student@localhost:5432/plantsdb'

db = SQLAlchemy()
'''
setup_db(app)
'''
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://student@localhost:5432/plantsdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app = app
    db.init_app(app)
    db.create_all()



class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    scientific_name = db.Column(db.String)
    is_poisonous = db.Column(db.String)
    primary_color = db.Column(db.String)

    def __init__(self, name, scientific_name, is_poisonous, primary_color):
        self.name = name
        self.scientific_name = scientific_name
        self.is_poisonous = is_poisonous
        self.primary_color = primary_color

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name':self.name,
            'scientific_name':self.scientific_name,
            'is_poisonous': self.is_poisonous,
            'primary_color':self.primary_color
        }    

