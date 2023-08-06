from .settings import settings
from .auth import Auth
import requests

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

class Email:
    id = None

    def __init__(self, email = None):
        self.id = email


    def Read():
        if not Auth.tokenValid():
            Auth.refreshToken()

        response = requests.get(settings.baseURL + 'api/message?type=email', headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            if "data" in response.json():
                return response.json()["data"]
            else:
                return []
        else:
            raise Exception(response.json()["message"])


    def ReadOne(self, extended = False):
        if not Auth.tokenValid():
            Auth.refreshToken()

        extended = str(extended).lower()
        response = requests.get(settings.baseURL + 'api/message/' + str(self.id) + '?extended=' + extended, headers={'Authorization': 'Bearer ' + settings.token})

        if response.json()["code"] is 200:
            return response.json()["data"]
        else:
            raise Exception(response.json()["message"])



    def Create(recipientname, recipientmail, mailsubject, content):
        if not Auth.tokenValid():
            Auth.refreshToken()

        # recipientname = "Bowen Harkema"
        # recipientmail = "newob01@hotmail.nl"
        # mailsubject = "Your Example Order Confirmation"

        message = Mail()

        message.to = [
            To(
                email = recipientmail,
                name = recipientname,
            ),
        ]
        message.from_email = From(
            email="info@clappform.com",
            name="Clappform",
        )
        message.subject = mailsubject

        message.content = [
            Content(
                mime_type="text/html",
                content=content
            )
        ]

        sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sendgrid_client.send(message)

        if response.json()["code"] is 202:
            return Email(id)
        else:
            raise Exception(response.json()["message"])
