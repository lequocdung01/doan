from typing import Any
from django.db import models

# Create your models here.
class Product(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    categy = models.CharField(max_length=200,null=True)
    sell = models.IntegerField()
    image = models.ImageField(null=True,blank=True)
    sale = models.IntegerField(null=True)
    def __str__(self):
        return self.name

class category(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name



