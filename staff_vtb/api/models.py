from django.db import models
from django.conf import settings

class Wallet(models.Model):
  private_key = models.CharField(
    max_length=2048
  )

  public_key = models.CharField(
    max_length=2048
  )

  def __str__(self):
    return "Кошелек: " + self.public_key

class Person(models.Model):
  user = models.OneToOneField(
    to=settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
  )

  wallet = models.OneToOneField(
    to=Wallet,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name="person"
  )

  def __str__(self):
    if self.user:
      return self.user.first_name + ' ' + self.user.last_name

    return "Не привязано"



class Team(models.Model):
  name = models.CharField(
    max_length=200
  )

  members = models.ManyToManyField(
    to=Person,
    null=True,
    blank=False,
  )

  def __str__(self):
    return self.name

class Challenge(models.Model):
  title = models.CharField(
    max_length=200,
    blank=False,
    null=True,
  )

  description = models.CharField(
    max_length=1024,
    blank=False,
    null=True,
  )

  instruction = models.CharField(
    max_length=1024,
    blank=True,
    null=True,
  )

  responsible = models.OneToOneField(
    to=Person,
    on_delete=models.CASCADE,
    blank=False,
    null=True,
    related_name="responsible"
  )

  users = models.ManyToManyField(
    to=Person,
    blank=False,
    null=True
  )

  def __str__(self):
    return self.title

class Achievement(models.Model):
  title = models.CharField(
    max_length=1024,
    blank=False,
    null=True,
  )

  description = models.CharField(
    max_length=1024,
    blank=False,
    null=True,
  )

  users = models.ManyToManyField(
    to=Person,
    null=True,
    blank=True,
  )

  reward = models.IntegerField()

  def __str__(self):
    if self.title:
      return self.title

    return 'Не указано'

