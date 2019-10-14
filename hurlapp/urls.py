# dappx/urls.py
from django.conf.urls import url
from hurlapp import views
# SET THE NAMESPACE!
# app_name = 'hurlapp'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^dashboard/$',views.dashboard,name='dashboard'),
    url(r'^get_user/$',views.get_manage_user,name='get_user'),
    url(r'^add_user/$',views.add_user,name='add_user'),
    url(r'^add_product/$',views.addProduct,name='add_product'),
    url(r'^add_order/$',views.addOrder,name='add_order'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]
