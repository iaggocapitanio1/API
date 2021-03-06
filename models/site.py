from __future__ import annotations
from SQL_Alchamy import dataBase
from typing import Union
from .hotel import HotelModel


class SiteModel(dataBase.Model):
    __tablename__ = 'sites'
    site_id = dataBase.Column(dataBase.Integer, primary_key=True)
    url = dataBase.Column(dataBase.String(80))
    hotels = dataBase.relationship('HotelModel')

    def __init__(self, url: str) -> None:
        self.url = url

    def getHotels(self) -> list[HotelModel]:
        return [hotel.json() for hotel in self.hotels]

    def json(self) -> dict:
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hotels': self.getHotels()
        }

    @classmethod
    def find_site(cls, url: str) -> Union[SiteModel, None]:
        site = cls.query.filter_by(url=url).first()  # SELECT * FROM sites WHERE site_id=site_is
        if site:
            return site
        return None

    @classmethod
    def find_by_id(cls, site_id: int) -> Union[SiteModel, None]:
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def save_site(self) -> None:
        dataBase.session.add(self)
        dataBase.session.commit()

    def delete_site(self) -> None:

        for hotel in self.hotels:
            hotel.delete_hotel()
        dataBase.session.delete(self)
        dataBase.session.commit()
