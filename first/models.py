from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# title = models.CharField(max_length=50, default='')


class Myname(models.Model):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
