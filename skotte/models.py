from django.db import models

class Station(models.Model):
    identifier = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)
    x = models.IntegerField()
    y = models.IntegerField()
    refreshed = models.DateTimeField(auto_now=True, auto_now_add=True)
