from rest_framework import serializers
from .models import Category, Product, Review, CustomUser, ConfirmationCode
from datetime import date
from django.contrib.auth.hashers import make_password, check_password


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()
    name = serializers.CharField(
        max_length=100,
        min_length=1,
        required=True,
        allow_blank=False,
        error_messages={
            'max_length': 'Название категории не может быть длиннее 100 символов.',
            'min_length': 'Название категории должно содержать хотя бы 1 символ.',
            'required': 'Название категории обязательно.',
            'blank': 'Название категории не может быть пустым.',
        }
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'products_count')

    def validate_name(self, value):
        if self.instance:
            if Category.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Категория с таким названием уже существует.")
        else:
            if Category.objects.filter(name__iexact=value).exists():
                raise serializers.ValidationError("Категория с таким названием уже существует.")
        
        if not value.replace(' ', '').replace('-', '').replace('_', '').isalnum():
            raise serializers.ValidationError("Названия категории должны содержать только буквы, цифры, пробелы, дефисы и подчеркивания.")
        
        return value.strip()


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            'required': 'Категория продукта обязательна.',
            'does_not_exist': 'Категория с ID {pk_value} не существует.',
            'invalid_pk_value': 'Значение "{data}" не является действительным ID категории.',
        }
    )
    
    name = serializers.CharField(
        max_length=255,
        min_length=1,
        required=True,
        allow_blank=False,
        error_messages={
            'max_length': 'Название продукта не может быть длиннее 255 символов.',
            'min_length': 'Название продукта должно содержать хотя бы 1 символ.',
            'required': 'Название продукта обязательно.',
            'blank': 'Название продукта не может быть пустым.',
        }
    )
    
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            'invalid': 'Описание должно быть строкой текста.',
        }
    )
    
    release_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'Дата выпуска обязательна.',
            'invalid': 'Дата выпуска должна быть в формате YYYY-MM-DD.',
        }
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={
            'required': 'Цена продукта обязательна.',
            'invalid': 'Цена должна быть числом.',
            'max_digits': 'Цена не может быть больше чем 10 цифр.',
            'max_decimal_places': 'Цена может иметь максимум 2 десятичных знака.',
        }
    )
    
    rating = serializers.FloatField(
        required=False,
        default=0,
        error_messages={
            'invalid': 'Рейтинг должен быть числом.',
        }
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'release_date', 'price', 'category', 'rating', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название продукта не может быть пустым.")
        
        forbidden_chars = ['<', '>', '{', '}', '|', '\\', '^', '`']
        if any(char in value for char in forbidden_chars):
            raise serializers.ValidationError("Название содержит недопустимые символы.")
        
        return value.strip()

    def validate_description(self, value):
        if value and len(value.strip()) == 0:
            return None
        return value

    def validate_release_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата выпуска не может быть в будущем.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        if value > 999999.99:
            raise serializers.ValidationError("Цена слишком высокая.")
        return value

    def validate_rating(self, value):
        if value < 0:
            raise serializers.ValidationError("Рейтинг не может быть отрицательным.")
        if value > 10:
            raise serializers.ValidationError("Рейтинг не может быть больше 10.")
        return value

    def validate(self, data):
        if not data.get('category'):
            raise serializers.ValidationError({'category': 'Категория продукта обязательна.'})
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        error_messages={
            'required': 'Продукт обязателен для отзыва.',
            'does_not_exist': 'Продукт с ID {pk_value} не существует.',
            'invalid_pk_value': 'Значение "{data}" не является действительным ID продукта.',
        }
    )
    
    text = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=5000,
        error_messages={
            'required': 'Текст отзыва обязателен.',
            'blank': 'Текст отзыва не может быть пустым.',
            'max_length': 'Текст отзыва не может быть длиннее 5000 символов.',
        }
    )
    
    star = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Рейтинг звезд обязателен.',
            'invalid': 'Рейтинг должен быть целым числом от 1 до 10.',
        }
    )

    class Meta:
        model = Review
        fields = ('id', 'product', 'text', 'star')

    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 3 символа.")
        
        if len(set(value)) <= 2:
            raise serializers.ValidationError("Текст отзыва содержит слишком много одинаковых символов.")
        
        return value.strip()

    def validate_star(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Рейтинг должен быть целым числом.")
        
        if value < 1 or value > 10:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 10.")
        
        return value

    def validate(self, data):
        if not data.get('product'):
            raise serializers.ValidationError({'product': 'Продукт обязателен для отзыва.'})
        
        return data


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(
        many=True,
        read_only=True
    )

    rating = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'release_date',
            'price',
            'category',
            'rating',
            'reviews',
            'created_at',
            'updated_at'
        )


# ============ USER AUTHENTICATION SERIALIZERS ============

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        error_messages={
            'required': 'Пароль обязателен.',
            'min_length': 'Пароль должен быть минимум 6 символов.',
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': 'Подтверждение пароля обязательно.',
        }
    )
    name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={
            'required': 'Имя обязательно.',
            'max_length': 'Имя не может быть длиннее 255 символов.',
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email обязателен.',
            'invalid': 'Email имеет неверный формат.',
        }
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'password_confirm')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя не может быть пустым.")
        return value.strip()

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают.'
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create(
            **validated_data,
            password=make_password(password),
            is_active=False
        )
        
        # Создаём код подтверждения
        code = ConfirmationCode.generate_code()
        ConfirmationCode.objects.create(
            user=user,
            code=code
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email обязателен.',
            'invalid': 'Email имеет неверный формат.',
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': 'Пароль обязателен.',
        }
    )

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        try:
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email не найден.'
            })

        if not check_password(password, user.password):
            raise serializers.ValidationError({
                'password': 'Неверный пароль.'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'email': 'Пожалуйста, подтвердите ваш email перед входом.'
            })

        data['user'] = user
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        required=True,
        error_messages={
            'required': 'Код подтверждения обязателен.',
            'min_length': 'Код должен быть 6 символов.',
            'max_length': 'Код должен быть 6 символов.',
        }
    )

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Код должен состоять только из цифр.")
        return value

    def validate(self, data):
        code = data.get('code')

        try:
            confirmation_code = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError({
                'code': 'Неверный код подтверждения.'
            })

        data['confirmation_code'] = confirmation_code
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_active', 'created_at')
        read_only_fields = ('id', 'is_active', 'created_at')
