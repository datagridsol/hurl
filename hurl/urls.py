from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from hurlapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.user_login,name='login'),
    url(r'^index/$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^',include('hurlapp.urls')),
    url(r'^logout/$', views.user_login, name='logout'),
    #url(r'^add_user$',views.addUser,name='addUser'),
    url(r'^accounts/login/', views.permission,name='permission'),
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 