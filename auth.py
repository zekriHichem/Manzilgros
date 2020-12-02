from flask import Flask , send_file, request , jsonify
from modals import *
import json
from flask_cors import CORS
import os
import bonTransfertInterne as bti
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Flask(__name__)
cors = CORS(app, resources={r"/*" : {"origin" : "*"}})
app.config["CROS_HEADERS"] = 'application/json'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"})
    if not password:
        return jsonify({"msg": "Missing password parameter"})
    a , token = User.login(username,password)
    if a == 0 :
        return  jsonify({"msg": "Invalid credentials!"})
    else:
        return jsonify(access_token=token), 200





if __name__ == '__main__':
    app.run(port=5004)