from django.db import models


class Todo(models.Model):
    task = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return "Task: %s" % self.task
