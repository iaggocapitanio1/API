from __future__ import annotations
from SQL_Alchamy import dataBase
from typing import Union


class UserModel(dataBase.Model):
    __tablename__ = 'users'
    user_id = dataBase.Column(dataBase.Integer, primary_key=True)
    login = dataBase.Column(dataBase.String(40))
    password = dataBase.Column(dataBase.String(40))

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    def json(self) -> dict:
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id: int) -> Union[UserModel, None]:
        user = cls.query.filter_by(user_id=user_id).first()  # SELECT * FROM users WHERE user_id=user_is
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login: str) -> Union[UserModel, None]:
        user = cls.query.filter_by(login=login).first()  # SELECT * FROM users WHERE user_id=user_is
        if user:
            return user
        return None

    def save_user(self) -> None:
        dataBase.session.add(self)
        dataBase.session.commit()

    def delete_user(self) -> None:
        dataBase.session.delete(self)
        dataBase.session.commit()
