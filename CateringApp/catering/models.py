from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class Diet(models.Model):
    number = models.CharField(max_length=3)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)
    calories = models.IntegerField()
    price_per_day = models.FloatField(default=0.0)
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.number} {self.name} {self.description} Calories: {self.calories} Price per day: {self.price_per_day}'


class Order(models.Model):
    user_name = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='orders')
    diet = models.ForeignKey(to=Diet, on_delete=models.PROTECT, related_name='orders')
    order_date_from = models.DateField()
    order_date_to = models.DateField()
    address = models.CharField(max_length=30)
    total_price = models.FloatField(default=0.0)

    def clean(self):
        if self.order_date_from < datetime.now().date():
            raise ValidationError("Order date must be today or in the future.")

        if self.order_date_from > self.order_date_to:
            raise ValidationError("Order end date must be equal to or after the start date.")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        days = (self.order_date_to - self.order_date_from).days
        self.total_price = self.diet.price_per_day * days
        super().save(force_insert, force_update, using, update_fields)


class ActivationCode(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="codes")
    date_created = models.DateTimeField(auto_now_add=True)
    date_expired = models.DateTimeField()
    code = models.CharField(max_length=255)