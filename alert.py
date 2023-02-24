from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import keys
from twilio.rest import Client

def send_mail_alert(app, subject, sender, recipients, body):
    mail = Mail(app)
    msg = Message(subject, sender, recipients)
    msg.body = body
    mail.send(msg)


def send_sms_alert(title, desc):
    client = Client(keys.account_sid, keys.auth_token)
    message = client.messages.create(
        body=title + ':' + desc,
        from_=keys.twilio_number,
        to=keys.target_number
    )
    print(message.body)