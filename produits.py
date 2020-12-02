from flask import Flask, request
from base import Session, engine, Base
from flask_cors import CORS
from modals import *
import json

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)
app = Flask(__name__)
cors = CORS(app, resources={r"/*" : {"origin" : "*"}})
app.config["CROS_HEADERS"] = 'application/json'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


@app.route('/hi')
@jwt_required
def hello_world():
    return 'Hello World!, From product'


@app.route('/get_all_products')
@jwt_required
def get_all_products():
    products =[ob.to_dict() for ob in Product.get_all()]
    print(products)
    return json.dumps(products)

@app.route('/get_one_product/<id>')
@jwt_required
def get_one_product(id):
    product = Product.get(id).to_dict()
    return product

@app.route('/add_product' , methods= ["POST"])
@jwt_required
def add_product():
    try:
        print("helooo")
        dataDict = json.loads(request.data)
        codebar = dataDict['codebar']
        ref = dataDict['ref']
        designation = dataDict['designation']
        quantite = dataDict['quantite']
        prix_vent = dataDict['prixVent']
        prix_achat = dataDict['prixAchat']
        famille = dataDict['famille']
        product = Product(codebar, ref, designation, quantite, prix_vent, prix_achat, famille)
        product.add()
        return Product(codebar, ref, designation, quantite, prix_vent, prix_achat, famille).to_dict()
    except:
        return Product("0","0","0",0,0,0,"0").to_dict()


@app.route('/update_product/<id>' , methods= ["POST"])
@jwt_required
def update_product(id):
    try:
        dataDict = json.loads(request.data)
        codebar = dataDict['codebar']
        ref = dataDict['ref']
        designation = dataDict['designation']
        quantite = dataDict['quantite']
        prix_vent = dataDict['prixVent']
        prix_achat = dataDict['prixAchat']
        famille = dataDict['famille']
        Product.update(id, codebar, ref, designation, quantite, prix_vent, prix_achat, famille)
        return Product(codebar, ref, designation, quantite, prix_vent, prix_achat, famille).to_dict()
    except:
        return Product("0","0","0",0,0,0,"0").to_dict()

@app.route('/add_all_products', methods= ["POST"])
@jwt_required
def add_all_products():
    try:
        print("hi from add all")
        f = request.files.get('excel')
        print("hi from add all")
        url = "media/PE/" + str(f.filename)
        f.save(url)
        products = Product.read_excel(url)
        Product.add_all(products)
        return "ok"
    except:
        return "error"

@app.route('/delete_product/<id>')
@jwt_required
def delete_product(id):
    print(id)
    Product.delete(int(id))
    return "ok"


if __name__ == '__main__':
    app.run(port=5001)
