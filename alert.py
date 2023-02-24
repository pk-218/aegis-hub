from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv

def send_mail_alert(app, subject, sender, recipients, body):
    mail = Mail(app)
    msg = Message(subject, sender, recipients)
    msg.body = body
    mail.send(msg)