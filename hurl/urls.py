from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from hurlapp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.user_login,name='login'),
    url(r'^index$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^hurlapp/',include('hurlapp.urls')),
    url(r'^logout/$', views.user_login, name='logout'),
    #url(r'^add_user$',views.addUser,name='addUser'),
    url(r'^accounts/login/', views.permission,name='permission'),
]
