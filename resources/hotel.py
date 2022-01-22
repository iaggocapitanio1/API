from flask_restful import Resource, reqparse
from models import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from .filter import normalize_path_args, query_with_city, query_without_city

# path /hotels?city=Rio-de-Janeiro&stars_min=3&daily_max=400

path_args = reqparse.RequestParser()
path_args.add_argument('city', type=str)
path_args.add_argument('stars_min', type=float)
path_args.add_argument('stars_max', type=float)
path_args.add_argument('daily_min', type=float)
path_args.add_argument('daily_max', type=float)
path_args.add_argument('limit', type=float)
path_args.add_argument('offset', type=float)


def get_valid_data(data: reqparse.Namespace) -> dict:
    return {key: data[key] for key in data.keys() if data[key] is not None}


class Hotels(Resource):
    def get(self):
        connection = sqlite3.connect('hotels.db')
        cursor = connection.cursor()

        data = path_args.parse_args()
        valid_data = get_valid_data(data)
        args = normalize_path_args(**valid_data)
        if not args.get('city'):
            query_args = tuple([args.get(key) for key in args.keys()])
            result = cursor.execute(query_without_city, query_args)
        else:

            query_args = tuple([args.get(key) for key in args.keys()])
            result = cursor.execute(query_with_city, query_args)
        hotels = list()
        for line in result:
            hotels.append({
                'hotel_id': line[0],
                'name': line[1],
                'stars': line[2],
                'daily': line[3],
                'city': line[4]
            }

            )
        return {'hotels': hotels}


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str, required=True, help='can not be empty')
    args.add_argument('stars', type=float, required=True, help='can not be empty')
    args.add_argument('daily')
    args.add_argument('city')
    args.add_argument('site_id', type=int, required=True, help="can not be empty")

    def get(self, hotel_id: str):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        else:
            return {'message': 'Hotel not found '}, 404

    @jwt_required()
    def post(self, hotel_id: str):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel {hotel_id} already exists.'}, 400
        data = self.args.parse_args()
        print(data)
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'an error occurred when trying to save. Please try again!'}, 500
        return hotel.json(), 200

    @jwt_required()
    def put(self, hotel_id: str):
        data = self.args.parse_args()
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found:
            hotel_found.update_hotel(**data)
            try:
                hotel_found.save_hotel()
            except:
                return {'message': 'an error occurred when trying to save. Please try again!'}, 500
            return hotel_found.json(), 200
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except Exception as e:
            print(e)
            return {'message': 'an error occurred when trying to save. Please try again!'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id: str):
        hotel = HotelModel.find_hotel(hotel_id=hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'an error occurred when trying to delete. Please try again!'}, 500
            return {'message': 'hotel deleted'}
        return {'message': 'hotel not found'}
