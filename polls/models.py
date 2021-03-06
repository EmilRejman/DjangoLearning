import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField(default=timezone.now) #auto_now_add=True, blank=True

    ordering = ['-pub_date']

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date' #by what field we sort
    was_published_recently.boolean = True #True or False changes to graphics
    was_published_recently.short_description = 'Published recently?' #what will be the column description


    class Meta: #defines what perrmisions what users can get
        #permissions = (("permision name", "permision display value"),)
        permissions = (("can_add_question", "allows user to add questions"),)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text