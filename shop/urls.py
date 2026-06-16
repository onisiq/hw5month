from django.contrib import admin
from django.urls import path
from product import views as product_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Product endpoints
    path('api/v1/products/', product_views.ProductListAPIView.as_view()),
    path('api/v1/products/<int:id>/', product_views.ProductDetailAPIView.as_view()),
    # Review endpoints
    path('api/v1/reviews/', product_views.ReviewListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', product_views.ReviewDetailAPIView.as_view()),
    # Category endpoints
    path('api/v1/categories/', product_views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', product_views.CategoryDetailAPIView.as_view()),
    # Product reviews endpoint
    path('api/v1/products/reviews/', product_views.ProductReviewsAPIView.as_view()),
    # Authentication endpoints
    path('api/v1/users/register/', user_views.UserRegistrationAPIView.as_view()),
    path('api/v1/users/login/', user_views.UserLoginAPIView.as_view()),
    path('api/v1/users/confirm/', user_views.UserConfirmAPIView.as_view()),
]
