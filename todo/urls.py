"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.db import router
from django.urls import path

from api.views import TodosView,TodosModelViews,UsersView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("todos",TodosView,basename="todos")
router.register("api/v1/todos",TodosModelViews,basename="mtodos")
router.register("api/v1/user",UsersView,basename="users")
#localhost:8000/todos/
#get
#localhost:8000/todos/1/
#get

urlpatterns = [
    path('admin/', admin.site.urls),
]+router.urls
