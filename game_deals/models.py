from django.db import models

# Create your models here.

class Deal(models.Model):
    game = models.CharField(max_length=200, unique=True)
    store = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    discount = models.CharField(max_length=5, default='N/A')
    link = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date reported')
    cover_hash = models.CharField(max_length=200, primary_key=True)
