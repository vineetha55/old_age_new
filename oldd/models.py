from django.db import models
from django.contrib.auth.models import User


class Registration(models.Model):
    password = models.CharField(max_length=200, null=True)
    user_role = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Category(models.Model):
    category_title = models.CharField(max_length=200, null=True)
    photo = models.ImageField(null=True)


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    discount = models.CharField(max_length=200, null=True)
    unit_price = models.CharField(max_length=200, null=True)
    prd_cat = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)