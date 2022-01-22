from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from models import UserModel
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('login', type=str, required=True, help='can not be empty')
args.add_argument('password', type=str, required=True, help='can not be empty')


class User(Resource):

    @staticmethod
    def get(user_id: int):
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        else:
            return {'message': 'user not found '}, 404

    @staticmethod
    @jwt_required()
    def delete(user_id: int):
        user = UserModel.find_user(user_id=user_id)
        if user:
            try:
                user.delete_user()
            except Exception as error:
                print(error)
                return {'message': 'an error occurred when trying to delete. Please try again!'}, 500
            return {'message': 'user deleted'}
        return {'message': 'user not found'}


class UserRegister(Resource):

    def post(self):
        data = args.parse_args()
        if UserModel.find_by_login(data['login']):
            return {'message': f"The login {data['login']} already exists"}

        user = UserModel(**data)
        try:
            user.save_user()
        except Exception as error:
            print(error)
            return {'message': 'an error occurred when trying to save. Please try again!'}, 500
        return {"message": "User created with success!"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()
        user = UserModel.find_by_login(data['login'])
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200
        return {'message': 'The username or password is incorrect'}, 401


class UserLogout(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout successfully!'}
