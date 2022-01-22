from typing import Union, Tuple, Dict

from flask_restful import Resource
from models import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):

    def get(self, url: str) -> Union[dict, tuple[dict[str, str], int]]:
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404

    def post(self, url: str) -> Union[dict, tuple[dict[str, str], int]]:
        site = SiteModel.find_site(url)
        if site:
            return {"message": "The site already exists"}, 400  # bad request
        site = SiteModel(url=url)
        try:
            site.save_site()
            return site.json(), 200
        except Exception as error:
            print(error)
            return {"message": "An intern error occurred when trying to save"}, 500

    def delete(self, url: str) -> tuple[dict[str: str], int]:
        site = SiteModel.find_site(url=url)
        if site:
            try:
                site.delete_site()
            except Exception as error:
                print(error)
                return {"message": "An error occurred when trying to delete!"}, 500
            return {"message": "site deleted"}, 200
        return {"message": "site not found"}, 404
