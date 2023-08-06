import datetime
from django.utils.timezone import localtime
from django.db.models import Q
import threading
import time
from django.utils import timezone

global seconds, tasks, ack


def calculate_seconds(task):
    task.date_time = localtime(task.date_time)
    task_time = datetime.datetime(task.date_time.year, task.date_time.month, task.date_time.day, task.date_time.hour,
                                  task.date_time.minute, task.date_time.second)
    current_time = datetime.datetime.now()
    return (task_time - current_time).seconds


def create_task_stack():
    from .models import TaskQueue
    global tasks
    tasks = []
    list(map(lambda task: tasks.append(task), TaskQueue.objects.filter(status__exact='waiting')))


def complete_pending_task():
    from .models import TaskQueue
    expire_task_queryset = TaskQueue.objects.filter(Q(status__exact='waiting') & Q(date_time__lt=timezone.now()))
    for task in expire_task_queryset:
        # change article status
        task.article.status = 'inactive' if task.article.status == 'active' else 'active'
        task.article.change_status_on = None
        task.article.save()
    expire_task_queryset.update(status='completed')
    create_task_stack()


def startup(wait):
    from .task import TaskEater
    global seconds, tasks, ack
    complete_pending_task()
    ack = False
    time.sleep(wait)
    while True:
        try:
            if 'TaskEater' not in list(map(lambda thread: type(thread).__name__, threading.enumerate())):
                ack = True
                latest_task = tasks[0]
                seconds = calculate_seconds(latest_task)
                worker = TaskEater('worker', latest_task)
                worker.setDaemon(True)
                worker.start()
            else:
                ack = True
                break
        except:
            break



