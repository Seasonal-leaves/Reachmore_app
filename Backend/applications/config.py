class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iescpmaindatabase.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'Rituparnoinfluencersposorapp'
    SECURITY_PASSWORD_SALT = 'rituparnoinfluencerpasswordsalt'

      # Celery Configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/1'  # You can change this to use a different broker like RabbitMQ
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'  # Change to your result backend if needed
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'  # Set to your desired timezone
    CELERY_ENABLE_UTC = True