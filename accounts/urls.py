"""django_crm_ivy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('account/', account_settings, name="account"),

    path('user/', userPage, name="user_page"),
    path('products/', products, name='products'),
    path('custumer/<str:pk>', custumer, name='customer'),
    path('create_order/<str:pk>', createOrder, name='create_order'),
    path('update_form/<str:pk>', updateOrder, name='update_order'),
    path('delete_order/<str:pk>', deleteOrder, name='delete_order'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_config"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
