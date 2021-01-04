# Create your models here.
import datetime
from django.db import models
from django.utils import timezone

class Quiz(models.Model):
    title_text = models.CharField(max_length=80)    
    description_text = models.CharField(max_length=800)
    pub_date = models.DateTimeField(verbose_name='date published', auto_now_add=True, blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title_text

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=320)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text