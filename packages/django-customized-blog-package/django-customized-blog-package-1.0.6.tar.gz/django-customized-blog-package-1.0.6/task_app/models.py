from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from blog.models import Article, AbstractCommonFields
from .choices import TASK_STATUS


class TaskQueue(AbstractCommonFields):
    status = models.CharField(max_length=10, choices=TASK_STATUS, default='waiting')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Task ID: {self.id} | Article: {self.article.title}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'TaskQueue'
        ordering = ['date_time', 'id']


@receiver(post_save, sender=TaskQueue)
def _post_save_receiver(sender, instance, *args, **kwargs):
    from task_app import utils
    utils.ack = False
    utils.startup(1)

