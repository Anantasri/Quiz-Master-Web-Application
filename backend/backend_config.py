class Config():
    SECRET_KEY = 'Quiz_master_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizmaster.db'
    
    SECURITY_PASSWORD_SALT = 'password_salt'
    
    CELERY_BROKEN_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'quizmaster1502@gmail.com'
    MAIL_PASSWORD = 'tqmp ecso npsw sdfq'
    MAIL_DEFAULT_SENDER = 'quizmaster1502@gmail.com'
    
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
