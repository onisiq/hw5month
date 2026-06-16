from django.db import models
from django.db.models import Avg
from django.contrib.auth.hashers import make_password
import random
import string


class Category(models.Model):
    name = models.CharField(max_length=100)

    @property
    def products_count(self):
        return self.product_set.count()
    
    @property
    def product_list(self):
        return [i.name for i in self.products.all()]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        return self.review_set.aggregate(
            Avg('star')
        )['star__avg']

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    star = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        default=5
    )

class CustomUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Code for {self.user.email}"
    
    @staticmethod
    def generate_code():
        """Генерирует 6-значный случайный код"""
        return ''.join(random.choices(string.digits, k=6))