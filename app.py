from typing import Tuple

from flask import Flask, jsonify, Response
from flask_restful import Api
from resources import Hotels, Hotel, User, UserRegister, UserLogin, UserLogout
from resources import Sites, Site, UserConfirm
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'V1QiLCJhbGciOiJIUzI1N'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=14)
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_db():
    dataBase.create_all()


@jwt.token_in_blocklist_loader
def verify_black_list(self, token) -> bool:
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalidated_token(jwt_header, jwt_payload) -> tuple[Response, int]:
    return jsonify({"message": "You have been logout"}), 401


api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(UserConfirm, '/confirm/<int:user_id>')

if __name__ == '__main__':
    from SQL_Alchamy import dataBase

    dataBase.init_app(app)
    app.run(debug=True)
