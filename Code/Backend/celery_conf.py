from flask import Flask
from celery import Celery, Task
from celery.schedules import crontab

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    celery_app.conf.beat_schedule = {
    'send_email-inactive': {
        'task': 'send_email',
        'schedule': crontab(minute="*"),
        # 'schedule': timedelta(minutes=1),
        },
        'monthly_report':{
            'task': 'monthly_report',
            'schedule': crontab(minute="*")
        },
        'revoke_access':{
            'task': 'revoke_access',
            'schedule': crontab(minute="*")
        },
        'delete_rej_issue': {
            'task': 'delete_rejected_issue_requests',
            'schedule': crontab(minute="*")
        }
    }
    return celery_app