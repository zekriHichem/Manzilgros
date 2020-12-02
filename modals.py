import datetime
from dataclasses import dataclass
from flask import jsonify
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Float, BLOB
from sqlalchemy.orm import relationship
from base import Session, engine, Base
from base import Base
import pandas as pd
import hashlib

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)
class Hi(Base):
    __tablename__ = 'Hil'
    id = Column(Integer,primary_key = True)
    t = Column(Integer)

    def __init__(self, t):
        self.t=t

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    @staticmethod
    def login(username, password):
        session = Session()
        user = session.query(User).filter(User.username == username).first()
        if user == None :
            return 0 , None
        if username != user.username or user.password != hashlib.sha256(password.encode("utf-8")).hexdigest():
            return 0, None
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username , expires_delta = datetime.timedelta(days=365))
        session.close()
        return 1 , access_token

    @staticmethod
    def register(username, password, confirmePassword):
        session = Session()
        if session.query(User).filter(User.username == username).first() == None :
            session.add(User(username=username, password= hashlib.sha256(password.encode("utf-8")).hexdigest()))
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key = True)
    codebar = Column(String, unique = True)
    ref = Column(String, unique= True)
    designation = Column(String)
    quantite = Column(Integer)
    prix_achat = Column(Float)
    prix_vent = Column(Float)
    famille = Column(String)
    factures = relationship("Facture_product", lazy='subquery',back_populates="product")
    receptions = relationship("Reception_product",lazy='subquery', back_populates="product")



    def __init__(self, codebar, ref, designation, quantite, prix_achat, prix_vent, famille):
        self.codebar = codebar
        self.ref = ref
        self.designation = designation
        self.quantite = quantite
        self.prix_vent = prix_vent
        self.prix_achat = prix_achat
        self.famille = famille
    @staticmethod
    def get_all():
        session = Session()
        products = session.query(Product).all()
        session.close()
        return products
    @staticmethod
    def get(id):
        session = Session()
        product = session.query(Product).get(id)
        session.close()
        return product
    @staticmethod
    def delete(id):
        product = Product.get(id)
        session = Session()
        session.delete(product)
        session.commit()
        session.close()
        return True
    def add(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()
        return self
    @staticmethod
    def update(id , codebar, ref, designation, quantite, prix_achat, prix_vent, famille):
        session = Session()
        product = session.query(Product).get(id)
        product.codebar = codebar
        product.ref = ref
        product.designation = designation
        product.quantite = quantite
        product.prix_vent = prix_vent
        product.prix_achat = prix_achat
        product.famille = famille
        session.commit()
        return product
    @staticmethod
    def add_all(products):
        session = Session()
        print("here")
        for product in products:
            session.add(product)
        session.commit()
        session.close()
        return products
    @staticmethod
    def read_excel(url):
        datafram = pd.read_excel(url)
        products = []
        for d in datafram.values :
            product = Product(str(d[0]), str(d[1]), str(d[2]), int(d[3]), float(d[4]), float(d[5]), d[6])
            products.append(product)
        return products
    def to_dict(self):
        return {'id': self.id, 'codebar': self.codebar, 'ref': self.ref,'designation' : self.designation,
                'quantite': self.quantite, 'prixAchat' : self.prix_achat,
                'prixVent' : self.prix_vent, 'famille': self.famille}

class Facture(Base):
    __tablename__ = 'Facture'
    id = Column(Integer, primary_key = True)
    date = Column(Date)
    products = relationship("Facture_product",lazy='subquery', back_populates="facture" ,cascade="all, delete")

    def __init__(self, date):
        self.date = date

    @staticmethod
    def get_all():
        session = Session()
        factures = session.query(Facture).all()
        session.close()
        return factures
    @staticmethod
    def get(id):
        session = Session()
        facture = session.query(Facture).get(id)
        session.close()
        return facture
    @staticmethod
    def delete(id):
        facture = Facture.get(id)
        session = Session()
        session.delete(facture)
        session.commit()
        session.close()
        return True
    def add(self, products):
        session =Session()
        product_err , idfact = product_facture(self,products,session)
        session.close()
        return idfact, product_err
    def to_dict(self):
        nb = len(self.products)
        return {'id' : self.id, 'date': self.date.__str__() , "nb_produit": nb}

class Reception(Base):
    __tablename__ = 'Reception'
    id = Column(Integer, primary_key = True)
    date = Column(Date)
    products = relationship("Reception_product",lazy='subquery', back_populates="reception",cascade="all, delete")

    def __init__(self, date):
        self.date = date
    @staticmethod
    def get_all():
        session = Session()
        receptions = session.query(Reception).all()
        session.close()
        return receptions
    @staticmethod
    def get(id):
        session = Session()
        reception = session.query(Reception).get(id)
        session.close()
        return reception
    @staticmethod
    def delete(id):
        reception = Reception.get(id)
        session = Session()
        session.delete(reception)
        session.commit()
        session.close()
        return True
    def add(self , products):
        print("here")
        session =Session()
        recp = product_reception(self, products, session)
        session.commit()
        session.close()
        return recp
    def to_dict(self):
        nb = len(self.products)
        return {'id' : self.id, 'date': self.date.__str__() , "nb_produit": nb}

class Facture_product(Base):
    __tablename__ = 'facture_product'
    left_id = Column(Integer, ForeignKey('Product.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('Facture.id'), primary_key=True)
    quantite = Column(Integer)
    facture = relationship("Facture", back_populates="products")
    product = relationship("Product", back_populates="factures")

class Reception_product(Base):
    __tablename__ = 'reception_product'
    left_id = Column(Integer, ForeignKey('Product.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('Reception.id'), primary_key=True)
    quantite = Column(Integer)
    reception = relationship("Reception", back_populates="products")
    product = relationship("Product", back_populates="receptions")


def product_reception(rec ,products, session):
    for p in products:
        p1 = session.query(Product).filter(Product.codebar == p.codebar).first()
        a = Reception_product(quantite=p.quantite)
        if p1 == None :
            session.add(p)
            session.commit()
            p2 = session.query(Product).filter(Product.codebar == p.codebar).first()
            a.product = p2
            rec.products.append(a)
        else:
            p1.quantite = p1.quantite + p.quantite
            a.product = p1
            rec.products.append(a)
    session.add(rec)
    session.commit()
    session.flush()
    return rec.id

def product_facture(fact, products, session):
    product_error = []
    for p in products:
        p1 = session.query(Product).filter(Product.codebar == p.codebar).first()
        if p1 == None:
            product_error.append(p)
        else:
            if p1.quantite - p.quantite < 0:
                product_error.append(p)
            else:
                a = Facture_product(quantite=p.quantite)
                a.product = p1
                fact.products.append(a)
                p1.quantite = p1.quantite - p.quantite
    session.add(fact)
    session.commit()
    session.flush()
    return product_error , fact.id
