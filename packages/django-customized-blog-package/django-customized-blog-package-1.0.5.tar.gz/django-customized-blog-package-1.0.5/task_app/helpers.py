from .serializers import TaskQueueSerializer
from .models import TaskQueue


def create_or_update_task(article):
    '''This function is to create or update task'''
    payload = {
        'article': article.id,
        'date_time': article.change_status_on
    }
    task = TaskQueue.objects.filter(article__id=article.id, status__exact='waiting').last()
    if task:
        serializer = TaskQueueSerializer(task, data=payload, partial=True)
    else:
        serializer = TaskQueueSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    print('Task does not create.')

