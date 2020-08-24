from django.db import models

# Create your models here.
class Date(models.Model):
    
    date = models.DateField()
    today = models.IntegerField()
    year_ago = models.IntegerField()
    