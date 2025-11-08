import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    
    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Hive connection settings
    HIVE_HOST = os.environ.get('HIVE_HOST') or 'localhost'
    HIVE_PORT = int(os.environ.get('HIVE_PORT') or 10000)
    HIVE_AUTH_MECHANISM = os.environ.get('HIVE_AUTH_MECHANISM') or 'PLAIN'
    HIVE_DATABASE = os.environ.get('HIVE_DATABASE') or 'healthcare'
    
    # API settings
    API_TIMEOUT = 300
    MAX_QUERY_LENGTH = 10000
    MAX_RESULTS = 10000
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
