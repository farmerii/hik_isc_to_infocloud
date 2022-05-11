"""park URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('car_upload', views.car_upload_view, name='car_upload'),
    path('car_list', views.car_list_view, name='car_list'),
    path('car_clear', views.car_clear_view, name='car_clear'),
    path('qunzu_upload', views.qunzu_upload_view, name='qunzu_upload'),
    path('qunzu_list', views.qunzu_list_view, name='qunzu_list'),
    path('qunzu_clear', views.qunzu_clear_view, name='qunzu_clear'),
    path('chezhu_upload', views.chezhu_upload_view, name='chezhu_upload'),
    path('chezhu_list', views.chezhu_list_view, name='chezhu_list'),
    path('chezhu_clear', views.chezhu_clear_view, name='chezhu_clear'),
    path('user_upload', views.user_upload_view, name='user_upload'),
    path('user_list', views.user_list_view, name='user_list'),
    path('user_clear', views.user_clear_view, name='user_clear'),
    path('yonghuxinxi_upload', views.yonghuxinxi_upload_view, name='yonghuxinxi_upload'),
    path('yonghuxinxi_list', views.yonghuxinxi_list_view, name='yonghuxinxi_list'),
    path('yonghuxinxi_clear', views.yonghuxinxi_clear_view, name='yonghuxinxi_clear'),
    path('zuzhixinxi_upload', views.zuzhixinxi_upload_view, name='zuzhixinxi_upload'),
    path('zuzhixinxi_list', views.zuzhixinxi_list_view, name='zuzhixinxi_list'),
    path('zuzhixinxi_clear', views.zuzhixinxi_clear_view, name='zuzhixinxi_clear'),
    path('tingguanjia', views.tingguanjia_view, name='tingguanjia'),
    path('tingguanjia_clear', views.tingguanjia_clear_view, name='tingguanjia_clear'),
    path('all_list', views.all_list_view, name='all_list'),
    path('all_download', views.all_download_view, name='all_download'),
]
