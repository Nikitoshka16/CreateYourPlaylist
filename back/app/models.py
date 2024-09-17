from django.db import models

class Musician(models.Model):
    id = models.BigIntegerField(primary_key=True)
    labelName = models.CharField(max_length=100)
    labelCountry = models.CharField(max_length=100)
    labelWebsite = models.TextField()
    labelEmail = models.CharField(max_length=100)
