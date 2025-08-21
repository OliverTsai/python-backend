import os

class Config:
    # 數據庫配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/company_search')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev_jwt_secret')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 1209600))  # 14天
    
    # 應用配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'