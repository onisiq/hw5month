from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# Reuse user-related models/serializers from the product app
from product.models import CustomUser, ConfirmationCode
from product.serializers import (
	UserRegistrationSerializer, UserLoginSerializer, ConfirmationCodeSerializer, UserSerializer
)


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
