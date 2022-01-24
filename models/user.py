from __future__ import annotations
from SQL_Alchamy import dataBase
from typing import Union
from flask import request, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

API_KEY = "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"


class UserModel(dataBase.Model):
    __tablename__ = 'users'
    user_id = dataBase.Column(dataBase.Integer, primary_key=True)
    login = dataBase.Column(dataBase.String(80), nullable=False, unique=True)
    password = dataBase.Column(dataBase.String(40), nullable=False)
    activated = dataBase.Column(dataBase.Boolean, default=False)
    email = dataBase.Column(dataBase.String(80), nullable=False, unique=True)

    def __init__(self, login: str, password: str, activated: bool, email: str) -> None:
        self.login = login
        self.password = password
        self.activated = activated
        self.email = email

    def json(self) -> dict:
        return {
            'user_id': self.user_id,
            'login': self.login,
            'activated': self.activated,
            'email': self.email
        }

    def getEmail(self) -> str:
        return self.email

    def send_confirmation_email(self) -> None:
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        print(self.email)
        message = Mail(
            from_email='iaggo.capitanio@gmail.com',
            to_emails=self.getEmail(),
            subject='Sending with Twilio SendGrid is Fun',
            plain_text_content=f" confirm: {link}",
            html_content=
            f"""
            <html>
             <p style="color: blue">Thanks for signing up</p>
             <a href={link}> Click Here to Confirm Your Email Address</a>
             </html>
            """)
        try:
            sg = SendGridAPIClient(API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as error:
            print(error)

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

    @classmethod
    def find_by_email(cls, email: str) -> Union[UserModel, None]:
        user = cls.query.filter_by(email=email).first()  # SELECT * FROM users WHERE user_id=user_is
        if user:
            return user
        return None

    def save_user(self) -> None:
        dataBase.session.add(self)
        dataBase.session.commit()

    def delete_user(self) -> None:
        dataBase.session.delete(self)
        dataBase.session.commit()
