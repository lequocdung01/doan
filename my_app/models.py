from typing import Any
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    categy = models.CharField(max_length=200,null=True)
    sell = models.IntegerField()

    def __str__(self):
        return self.name