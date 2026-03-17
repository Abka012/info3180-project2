import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'DriftDater$ec5etK3y2024!')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    MAILTRAP_SMTP_HOST = os.environ.get('MAILTRAP_SMTP_HOST', 'sandbox.smtp.mailtrap.io')
    MAILTRAP_SMTP_PORT = int(os.environ.get('MAILTRAP_SMTP_PORT', 2525))
    MAILTRAP_SMTP_USER = os.environ.get('MAILTRAP_SMTP_USER')
    MAILTRAP_SMTP_PASS = os.environ.get('MAILTRAP_SMTP_PASS')
    MAILTRAP_FROM_EMAIL = os.environ.get('MAILTRAP_FROM_EMAIL', 'DriftDater <noreply@driftdater.com>')
