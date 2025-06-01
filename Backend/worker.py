from celery_worker import create_celery_app  # Import Celery initialization
from main import create_app

# Initialize Flask app and Celery
app, api, celery_app = create_app()  # Use the Flask app context

# Celery initialization using the separate `celery_worker.py`
celery_app = create_celery_app()  # Now we use the app's Celery instance directly

class FlaskTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
        # Use Flask app context when running Celery tasks
        with app.app_context():
            return self.run(*args, **kwargs)
