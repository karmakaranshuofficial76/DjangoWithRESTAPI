from django.db import models

# Create your models here.


class MyFiles(models.Model):
    image = models.ImageField()

