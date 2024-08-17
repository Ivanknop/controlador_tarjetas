import os 
import csv

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import requests,json
from flask import Flask

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///super_hero.db")
base = declarative_base()
app=Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///super_hero.db"
#from config import config

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
name_file = 'lista_de_personajes_estadisticas_pd.csv'
config_path_name = os.path.join(script_path, name_file)

db= SQLAlchemy()
db.init_app(app)

class Hero(base):
    __tablename__ = "hero"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    inteligencia = db.Column(db.Float)
    fuerza = db.Column(db.Float)
    velocidad = db.Column(db.Float)
    dureza = db.Column(db.Float)
    poder =  db.Column(db.Float)
    combate = db.Column(db.Float)
    total = db.Column(db.Float)
    vida = db.Column(db.Float)

    def get_name(self):
        return self.nombre
    def get_intelligence(self):
        return self.inteligencia
    def get_strong(self):
        return self.fuerza
    def get_speed(self):
        return self.velocidad
    def get_toughness(self):
        return self.dureza
    def get_power(self):
        return self.poder
    def get_combat(self):
        return self.combate
    def get_total_power(self):
        return self.total
    def get_life(self):
        return self.vida
        
def create_schema():
    # Crear las tablas
    base.metadata.create_all(engine)

def drop_schema():
    # Borrar todos las tablas existentes en la base de datos
    base.metadata.drop_all(engine)

def insert_hero(nombre, inteligencia, fuerza, velocidad, dureza, poder, combate, total, vida):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo héroe
    a_hero = Hero(nombre=nombre, inteligencia=inteligencia, fuerza=fuerza, velocidad=velocidad, dureza=dureza, poder=poder, combate=combate, total=total, vida=vida)

    # Agregar el héroe a la DB
    db.session.add(a_hero)
    db.session.commit()
    

def fill():
    # Insertar el archivo CSV de heroes
    # Insertar todas las filas juntas
    with open(config_path_name, 'r', encoding='utf8') as fi:
        data = list(csv.DictReader(fi))

        for row in data:
            insert_hero(row['NOMBRE'], row['INT'], row['FUE'], row['VEL'], row['DUR'], row['POD'], row['COMBATE'], row['Total'], row['VIDA'])

def show(limit=0, offset=0):
    list_hero = []
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar todas las personas
    query = db.session.query(Hero).order_by(Hero.nombre.asc())

    # Si está definido el limite aplicarlo
    if limit > 0:
        query = query.limit(limit)
        if offset>0:
            query = query.offset(offset)

    # Leer una persona a la vez e imprimir en pantalla
    for hero in query:
        list_hero.append(hero)
    return list_hero

def find_hero(name,limit=0, offset=0):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()
    # Buscar el héroe que se desea 
    query = db.session.query(Hero).filter(Hero.nombre == name)
    if limit > 0:
        query = query.limit(limit)
        if offset>0:
            query = query.offset(offset)

    a_hero = query.first()
    if a_hero:
        return a_hero
    else:
        return (f'{name} no se encuentra en la BD')

def delete_hero(name):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Borrar el héroe con nombre "name"
    session.query(Hero).filter(Hero.nombre == name).delete()
    session.commit()

    print(f'{name} ya no se encuentra en la BD')

find_hero('batman')