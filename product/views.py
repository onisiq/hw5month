from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Product, Review, Category, CustomUser, ConfirmationCode
from .serializers import (
    ProductSerializer, ReviewSerializer, CategorySerializer, ProductReviewSerializer,
    UserRegistrationSerializer, UserLoginSerializer, ConfirmationCodeSerializer, UserSerializer
)

# Create your views here.

# ============ PRODUCT VIEWS ============

class ProductListAPIView(APIView):
    """
    GET: Получить все продукты
    POST: Создать новый продукт (валидация: name, price > 0, release_date, category exists)
    """
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        # Проверка на пустой запрос
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


class ProductDetailAPIView(APIView):
    """
    GET: Получить детали продукта
    PUT: Обновить продукт (валидация: name, price > 0, release_date, category exists)
    DELETE: Удалить продукт
    """
    
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None
    
    def get(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {'error': f'Продукт с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, many=False)
        return Response(data=serializer.data)
    
    def put(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {'error': f'Продукт с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
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
    
    def delete(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {'error': f'Продукт с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(
            {'message': 'Продукт успешно удален.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============ REVIEW VIEWS ============

class ReviewListAPIView(APIView):
    """
    GET: Получить все отзывы
    POST: Создать новый отзыв (валидация: text not empty, star 1-10, product exists)
    """
    
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        # Проверка на пустой запрос
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


class ReviewDetailAPIView(APIView):
    """
    GET: Получить детали отзыва
    PUT: Обновить отзыв (валидация: text not empty, star 1-10, product exists)
    DELETE: Удалить отзыв
    """
    
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None
    
    def get(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {'error': f'Отзыв с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(review, many=False)
        return Response(data=serializer.data)
    
    def put(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {'error': f'Отзыв с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
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
    
    def delete(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {'error': f'Отзыв с ID {id} не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        review.delete()
        return Response(
            {'message': 'Отзыв успешно удален.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============ CATEGORY VIEWS ============

class CategoryListAPIView(APIView):
    """
    GET: Получить все категории
    POST: Создать новую категорию (валидация: name not empty, unique name)
    """
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        # Проверка на пустой запрос
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


class CategoryDetailAPIView(APIView):
    """
    GET: Получить детали категории
    PUT: Обновить категорию (валидация: name not empty, unique name)
    DELETE: Удалить категорию
    """
    
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None
    
    def get(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(
                {'error': f'Категория с ID {id} не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, many=False)
        return Response(data=serializer.data)
    
    def put(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(
                {'error': f'Категория с ID {id} не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
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
    
    def delete(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(
                {'error': f'Категория с ID {id} не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response(
            {'message': 'Категория успешно удалена.'},
            status=status.HTTP_204_NO_CONTENT
        )


# ============ PRODUCT REVIEWS VIEW ============

class ProductReviewsAPIView(APIView):
    """
    GET: Получить все продукты со всеми их отзывами
    """
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductReviewSerializer(products, many=True)
        return Response(data=serializer.data)


# ============ AUTHENTICATION VIEWS ============

class UserRegistrationAPIView(APIView):
    """
    POST: Регистрация нового пользователя
    При регистрации пользователь неактивен и ему отправляется 6-значный код подтверждения
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = ConfirmationCode.objects.get(user=user)
            return Response(
                {
                    'message': 'Пользователь успешно зарегистрирован. Проверьте ваш email на наличие кода подтверждения.',
                    'data': UserSerializer(user).data,
                    'code': confirmation_code.code  # В реальности это отправилось бы на email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginAPIView(APIView):
    """
    POST: Авторизация пользователя
    Требует email и пароль
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            return Response(
                {
                    'message': 'Вы успешно вошли в систему.',
                    'data': UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserConfirmAPIView(APIView):
    """
    POST: Подтверждение пользователя по коду
    Требует 6-значный код подтверждения
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        if not request.data:
            return Response(
                {'error': 'Тело запроса не может быть пустым.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data.get('confirmation_code')
            user = confirmation_code.user
            
            # Активируем пользователя
            user.is_active = True
            user.save()
            
            # Удаляем код подтверждения
            confirmation_code.delete()
            
            return Response(
                {
                    'message': 'Пользователь успешно подтвержден.',
                    'data': UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        