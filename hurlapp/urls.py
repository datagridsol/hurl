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
    url(r'^edit_user/(?P<pk>\d+)$',views.edit_user,name='edit_user'),
    url(r'^get_retailer/$',views.get_retailer,name='get_retailer'),
    url(r'^add_retailer/$',views.add_retailer,name='add_retailer'),
     url(r'^edit_retailer/(?P<pk>\d+)$',views.edit_retailer,name='edit_retailer'),
     url(r'^get_farmer/$',views.get_farmer,name='get_farmer'),
    url(r'^add_farmer/$',views.add_farmer,name='add_farmer'),
    url(r'^edit_farmer/(?P<pk>\d+)$',views.edit_farmer,name='edit_farmer'),
    url(r'^get_wholesaler/$',views.get_wholesaler,name='get_wholesaler'),
    url(r'^add_wholesaler/$',views.add_wholesaler,name='add_wholesaler'),
    url(r'^edit_wholesaler/(?P<pk>\d+)$',views.edit_wholesaler,name='edit_wholesaler'),
    url(r'^import_wholesaler/$',views.import_wholesaler,name='import_wholesaler'),
    url(r'^search_city/$',views.search_city,name='search_city'),

    url(r'^add_product/$',views.add_product,name='add_product'),
    url(r'^get_product/$',views.get_product,name='get_product'),
    url(r'^add_order/$',views.addOrder,name='add_order'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_status/$',views.user_status,name='user_status'),
    url(r'^mobile_login/$',mobilefunctions.login,name='mobile_login'),
    url(r'^check_login/$',mobilefunctions.check_login,name='check_login'),
    url(r'^add_user_mobile/$',mobilefunctions.add_user_mobile,name='add_user_mobile'),
    url(r'^get_wholesaler_list/$',mobilefunctions.get_wholesaler,name='get_wholesaler_list'),
    url(r'^get_product_list/$',mobilefunctions.get_product_mobile,name='get_product_mobile'),
    url(r'^get_district/$',views.get_district,name='get_district'),
    # url(r'^testimage/$',views.SaveProfile,name='testimage'),
    

]


