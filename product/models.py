from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100)

    @property
    def count_products(self):
        return self.products.count()

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
        on_delete=models.CASCADE
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
    text = models.TextField()
    star = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        default=5
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text