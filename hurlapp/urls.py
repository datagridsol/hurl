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
    url(r'^check_user_mobile/$',views.check_user_mobile,name='check_user_mobile'),
    url(r'^user_profile/(?P<pk>\d+)$',views.user_profile,name='user_profile'),
    url(r'^edit_product/(?P<pk>\d+)$',views.edit_product,name='edit_product'),
    url(r'^check_aadhar_card/$',views.check_aadhar_card,name='check_aadhar_card'),

    # url(r'^add_state/$',views.add_state,name='add_state'),
    url(r'^add_product/$',views.add_product,name='add_product'),
    url(r'^get_product/$',views.get_product,name='get_product'),
    url(r'^add_order/$',views.addOrder,name='add_order'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_status/$',views.user_status,name='user_status'),
    url(r'^product_status/$',views.product_status,name='product_status'),
    url(r'^mobile_login/$',mobilefunctions.login,name='mobile_login'),
    url(r'^check_login/$',mobilefunctions.check_login,name='check_login'),
    url(r'^add_user_mobile/$',mobilefunctions.add_user_mobile,name='add_user_mobile'),
    url(r'^get_wholesaler_list/$',mobilefunctions.get_wholesaler,name='get_wholesaler_list'),
    url(r'^get_product_list/$',mobilefunctions.get_product_mobile,name='get_product_mobile'),
    url(r'^get_district/$',views.get_district,name='get_district'),
    url(r'^get_district_list/$',mobilefunctions.get_district_list,name='get_district_list'),
    url(r'^get_state_list/$',mobilefunctions.get_state_list,name='get_state_list'),
    url(r'^get_city_list/$',mobilefunctions.get_city_list,name='get_city_list'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    url(r'^manage_contain/$',mobilefunctions.all_manage_contain,name='all_manage_contain'),
    url(r'^add_user_mobile/$',mobilefunctions.add_user_mobile,name='add_user_mobile'),
    url(r'^check_phone_no/$',mobilefunctions.get_username,name='check_phone_no'),
    url(r'^get_farmer_list/$',mobilefunctions.get_farmer_list,name='get_farmer_list'),
    url(r'^add_order_list/$',mobilefunctions.add_order_list,name='add_order_list'),
    
    # url(r'^testimage/$',views.SaveProfile,name='testimage'),

]


