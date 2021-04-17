from django.contrib.auth.models import User
from django.db import models


class Walk(models.Model):
    name = models.CharField(max_length=20, default='')
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    link = models.CharField(max_length=1000)
    rate = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class Option(models.Model):
    text = models.CharField(max_length=500)
    voting = models.ForeignKey(Walk, on_delete=models.PROTECT)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    option = models.ForeignKey(Option, on_delete=models.PROTECT)
    walk = models.ForeignKey(Walk, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    text = models.CharField(max_length=50)
    walks = models.ManyToManyField(Walk, related_name='tag')


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now=True)
    walk = models.ForeignKey(Walk, on_delete=models.CASCADE)
