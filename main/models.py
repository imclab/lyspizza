from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Pizzeria(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class ItemCategory(models.Model):
    name = models.CharField(max_length=100)
    index = models.IntegerField()
    pizzeria = models.ForeignKey(Pizzeria)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    pizzeria = models.ForeignKey(Pizzeria)
    category = models.ForeignKey(ItemCategory)

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    price = models.IntegerField()
    ingredients = models.CharField(max_length=255)

    onlinepizza_id = models.IntegerField()

    def __unicode__(self):
        return '%s: %s. %s' % (self.category.name, self.number, self.name)

class Occasion(models.Model):
    date = models.DateField()
    pizzeria = models.ForeignKey(Pizzeria)

    def __unicode__(self):
        return str(self.date)
    
class Attendance(models.Model):
    occasion = models.ForeignKey(Occasion)
    user = models.ForeignKey(User)
    items = models.ManyToManyField(Item)
    notes = models.TextField()
    paid = models.BooleanField()

    def __unicode__(self):
        return '%s: %s' % (str(self.occasion.date), self.user.username)

class AttendanceLogEntry(models.Model):
    attendance = models.ForeignKey(Attendance)
    text = models.TextField()


# Forms

#class LoginForm(forms.Form):
#    username = forms.
#    password = 
