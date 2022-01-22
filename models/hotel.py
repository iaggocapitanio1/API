from __future__ import annotations
from SQL_Alchamy import dataBase
from typing import Union


class HotelModel(dataBase.Model):
    __tablename__ = 'hotels'
    hotel_id = dataBase.Column(dataBase.String, primary_key=True)
    name = dataBase.Column(dataBase.String(80))
    stars = dataBase.Column(dataBase.Float(precision=1))
    daily = dataBase.Column(dataBase.Float(precision=2))
    city = dataBase.Column(dataBase.String(20))
    site_id = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id: str, name: str, stars: float, daily: float, city: str, site_id: int) -> None:
        self.hotel_id = hotel_id
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city
        self.site_id = site_id

    def json(self) -> dict:
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'daily': self.daily,
            'city': self.city,
            'site_id': self.site_id
        }

    @classmethod
    def find_hotel(cls, hotel_id: str) -> Union[HotelModel, None]:
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()  # SELECT * FROM hotels WHERE hotel_id=hotel_is
        if hotel:
            return hotel
        return None

    def save_hotel(self) -> None:
        dataBase.session.add(self)
        dataBase.session.commit()

    def update_hotel(self, name: str, stars: float, daily: float, city: str, site_id: url):
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city
        self.site_id = site_id

    def delete_hotel(self) -> None:
        dataBase.session.delete(self)
        dataBase.session.commit()
