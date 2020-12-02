from flask import Flask , send_file, request
from modals import *
import json
from flask_cors import CORS
import os
import bonTransfertInterne as bti
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)
app = Flask(__name__)
cors = CORS(app, resources={r"/*" : {"origin" : "*"}})
app.config["CROS_HEADERS"] = 'application/json'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

@app.route('/facture')
@jwt_required
def hello_world():
    return "Hello world!, From Facture"

@app.route('/facture/get_all_factures')
@jwt_required
def get_all_factures():
    factures = [ob.to_dict() for ob in Facture.get_all()]
    return json.dumps(factures)

@app.route('/facture/delete_facture/<id>')
@jwt_required
def delete_facture(id):
    Facture.delete(id)
    return "ok"

@app.route('/facture/add_facture' , methods= ["POST"])
@jwt_required
def add_facture():
    f = request.files['excel']
    url = "media/FEB/" + str(f.filename)
    f.save(url)
    fact, pe = Facture(request.form.get("date")).add(Product.read_excel(url))
    os.rename(url,r'media/FEB/fact' + str(fact) + '.xlsx')
    bti.run(Product.read_excel(r'media/FEB/fact' + str(fact) + '.xlsx'), fact)
    return fact.__str__()

@app.route('/facture/products_facture/<id>')
@jwt_required
def products_facture(id):
    products = [ob.to_dict() for ob in Facture.get(id).products]
    return json.dumps(products)

@app.route('/facture/file_excel/<id>')
def file_excel(id):
    return send_file('media/FEB/fact'+ id + '.xlsx')

@app.route('/facture/file_docx/<id>')
def file_docx(id):
    return send_file('media/BTI/fact'+ id + '.docx')

if __name__ == '__main__':
    app.run(port=5002)