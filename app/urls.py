"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt 
from django.urls import path
from . import views
from app.schema import schema
from graphene_django.views import GraphQLView

urlpatterns = [
    path('',views.HomePage,name='home'),
    path('signup',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('loginapi/',views.LoginApi,name='loginapi'),
    path('logoutapi/',views.LogoutApi,name='logoutapi'),
    path('home/',views.HomePage,name='home'),
    path('cart/',views.Cart,name='cart'),
    path('checkout/',views.Checkout,name='checkout'),
    path('profile/',views.Profile,name='profile'),
    path('logout/',views.LogoutPage,name='logout'),
    path('productapi/',views.ProductApi,name='productapi'),

    path("thirdparty", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("productsgraphqlapi", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
