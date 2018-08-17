from django.db import models

# Create your models here.

class Deal(models.Model):
    game = models.CharField(max_length=200)
    store = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    discount = models.CharField(max_length=5, default='N/A')
    link = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date reported')
