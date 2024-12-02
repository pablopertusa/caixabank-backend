import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "pablo27")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@mysql:3306/bankingapp")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "pablo27")
