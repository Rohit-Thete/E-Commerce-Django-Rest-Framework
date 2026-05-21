from .views import register, login_user, UserView, CategoryView, ProductView, OrderView
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("category", CategoryView, basename="category")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register),
    path("login/", login_user),
    path("user/", UserView.as_view()),
    
    # path("category/", CategoryView.as_view()),
    # path("category/<int:pk>/", CategoryView.as_view()),
    path("product/", ProductView.as_view()),
    path("product/<int:pk>/", ProductView.as_view()),
    path("order/", OrderView.as_view()),
    path("order/<int:pk>/", OrderView.as_view()),
    path("order/cancel/<int:pk>", OrderView.as_view()),
]
