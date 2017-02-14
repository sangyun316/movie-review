from django.conf.urls import url
# from views import index, login, register, success, logout
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^success$', views.success, name='success'),
    url(r'^logout$', views.logout, name='logout'),
]
