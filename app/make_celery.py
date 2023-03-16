from celery import current_app as current_celery_app


def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")  # Configures the Celery application instance using
    #                                                           the Flask application's configuration options.
    #                                                           The namespace argument specifies that the Celery
    #                                                           options should be prefixed with "CELERY_" to avoid
    #                                                           conflicts with other Flask options.

    return celery
