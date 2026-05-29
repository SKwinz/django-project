from django.db import models
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name

    
    def clean(self):
        if self.pk and self.employees.count() == 0:
            raise ValidationError("Project must have at least one employee")

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=100)
    date_joined = models.DateField()

    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='employees'
    )

    def __str__(self):
        return self.name