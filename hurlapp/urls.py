# dappx/urls.py
from django.conf.urls import url
from hurlapp import views,mobilefunctions
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
    url(r'^mobile_login/$',mobilefunctions.login,name='mobile_login'),
    url(r'^check_login/$',mobilefunctions.check_login,name='check_login'),
    url(r'^get_district/$',views.get_district,name='get_district'),
    url(r'^testimage/$',views.hotel_image_view,name='testimage'),

]
