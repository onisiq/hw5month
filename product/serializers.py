from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(
        source='review_set',
        many=True,
        read_only=True

    )

    rating = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = '__all__'



