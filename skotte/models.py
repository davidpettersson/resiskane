from django.db import models

class Station(models.Model):
    identifier = models.IntegerField(unique=True)
    name = models.CharField(max_length=256, db_index=True)
    x = models.IntegerField()
    y = models.IntegerField()
    metaphone = models.CharField(max_length=128, db_index=True)
    refreshed = models.DateTimeField(auto_now=True, auto_now_add=True)
