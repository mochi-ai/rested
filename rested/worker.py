from celery import Celery
from celery.schedules import crontab # import for convience


# create celery worker app
app = Celery('rested')
app.config_from_object('django.conf:settings', namespace='CELERY')

# create a background task
task = app.task

# create a scheduled task
def scheduled_task(time, args=None, soft_time_limit=None, time_limit=None):

    # check time limit arguments
    if time_limit:
        assert soft_time_limit < time_limit, "soft_time_limit should be less than time_limit"
        assert time_limit < time.total_seconds(), "time_limit should be less than 'time', the call period"

    # create decorator
    def decorator(func):

        # add func as task
        tsk = app.task(func)
        if time_limit or soft_time_limit:
            tsk.soft_time_limit = soft_time_limit
            tsk.time_limit = time_limit

        # add task to schedule
        label = func.__module__ + '.' + func.__name__
        schd = app.conf.CELERYBEAT_SCHEDULE
        schd[label] = {'task': label, 'schedule': time, 'args': args}
                                        # removing for now, but keeping comment in case there was some reason
        # update runner's schedule
        app.conf.update(CELERYBEAT_SCHEDULE=schd)
        return func
    return decorator
