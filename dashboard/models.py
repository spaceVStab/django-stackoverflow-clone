# python manage.py makemigrations
# python manage.py migrate

from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Questions(models.Model):
    ques_text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    # upvotes = models.SmallIntegerField()
    ques_title = models.TextField()
    posted_by = models.ForeignKey(User, default=None, on_delete=CASCADE)

class Answers(models.Model):
    ans_text = models.TextField()
    answered_by =  models.ForeignKey(User, default=None, on_delete=CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Questions, default=None, on_delete=CASCADE)
    # upvotes = models.SmallIntegerField()