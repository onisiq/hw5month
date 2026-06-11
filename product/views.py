from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Review, Category
from .serializers import ProductSerializer, ReviewSerializer, CategorySerializer, ProductReviewSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            {'error': f'Продукт с ID {id} не найден.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(data=serializer.data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(
            {'message': 'Продукт успешно удален.'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Продукт успешно обновлен.', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Продукт успешно создан.', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            {'error': f'Отзыв с ID {id} не найден.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review, many=False)
        return Response(data=serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(
            {'message': 'Отзыв успешно удален.'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Отзыв успешно обновлен.', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Отзыв успешно создан.', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(
            {'error': f'Категория с ID {id} не найдена.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = CategorySerializer(category, many=False)
        return Response(data=serializer.data)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(
            {'message': 'Категория успешно удалена.'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Категория успешно обновлена.', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Категория успешно создана.', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductReviewSerializer(products, many=True)
    return Response(data=serializer.data)
