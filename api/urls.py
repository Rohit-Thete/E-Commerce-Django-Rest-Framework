from .views import register,login_user,UserView
from django.urls import path

urlpatterns = [
    path('register/',register),
    path('login/',login_user),
    path('user/',UserView.as_view()),

]
