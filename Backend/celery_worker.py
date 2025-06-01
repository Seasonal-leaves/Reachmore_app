# celery_worker.py

from celery import Celery
from applications.config import Config

def create_celery_app():
    # Create and configure the Celery app instance
    celery = Celery(
        'iescp',  # Use your app name or 'iescp' as the Celery instance name
        backend=Config.CELERY_RESULT_BACKEND, 
        broker=Config.CELERY_BROKER_URL
    )
    # Configure Celery from Flask config
    celery.config_from_object(Config)
    return celery
