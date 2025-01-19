from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=200)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE) 
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'units'

    def __str__(self):
        return self.name





        