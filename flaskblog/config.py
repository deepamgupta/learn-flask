import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # It is a random string; Provides a protection from hackers
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')  # email-id
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')  # email-password
