from flask import Flask, send_file, request
import os
from modals import *
import json
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)
app = Flask(__name__)
cors = CORS(app, resources={r"/*" : {"origin" : "*"}})
app.config["CROS_HEADERS"] = 'application/json'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

@app.route('/reception')
@jwt_required
def hello_world():
    return "Hello world!, From Reception"

@app.route('/reception/get_all_receptions')
@jwt_required
def get_receptions():
    receptions = [ob.to_dict() for ob in Reception.get_all()]
    return json.dumps(receptions)


@app.route('/reception/delete_reception/<id>')
@jwt_required
def delete_reception(id):
    Reception.delete(id)
    return {'res':"ok"}

@app.route('/reception/add_reception' , methods= ["POST"])
@jwt_required
def add_reception():
    f = request.files.get("excel")
    url = "media/REB/" + str(f.filename)
    f.save(url)
    reception = Reception(request.form.get("date"))
    recp = reception.add(Product.read_excel(url))
    os.rename(url, r'media/REB/rec' + str(recp) + '.xlsx')
    return recp.__str__()

@app.route('/reception/products_reception/<id>')
@jwt_required
def products_reception(id):
    products = [json.dumps([ob.to_dict() for ob in Facture.get(id).products])]
    return json.dumps(products)

@app.route('/reception/file_excel/<id>')
def file_excel(id):
    return send_file('media/REB/rec' + id + '.xlsx')

if __name__ == '__main__':
    app.run(port=5003)