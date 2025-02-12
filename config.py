# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IVF3SHGD&T457GASSD2I'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:02apr1978@127.0.0.1:3306/mula'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
