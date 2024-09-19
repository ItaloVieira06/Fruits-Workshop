from django.db import models

# Create your models here.

#tabela de frutas
class Fruits(models.Model):
    CLASSIFICATION_CHOICES = {
          "Extra": "extra",
          "Primeira": "primeira",
          "Segunda": "segunda",
          "Terceira": "terceira",
     }

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    clas = models.CharField(max_length = 10, choices = CLASSIFICATION_CHOICES, blank = False, null = False)
    fresh = models.BooleanField()
    quant = models.IntegerField()
    value = models.FloatField()

class Sell(models.Model):

    id = models.AutoField(primary_key=True)
    salesman = models.CharField(max_length=20, default="nome")
    products = models.CharField(max_length= 10, blank=False, null=False)
    hour = models.CharField(max_length=15)
    value = models.FloatField()