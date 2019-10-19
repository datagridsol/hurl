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
    url(r'^add_product/$',views.add_product,name='add_product'),
    url(r'^get_product/$',views.get_product,name='get_product'),
    url(r'^add_order/$',views.addOrder,name='add_order'),
    url(r'^user_login/$',views.user_login,name='user_login'),
<<<<<<< HEAD
    url(r'^user_status/$',views.user_status,name='user_status'),
    url(r'^mobile_login/$',mobilefunctions.login,name='mobile_login'),
    url(r'^check_login/$',mobilefunctions.check_login,name='check_login'),
    url(r'^add_user_mobile/$',mobilefunctions.add_user_mobile,name='add_user_mobile'),
    url(r'^get_district/$',views.get_district,name='get_district'),
    # url(r'^testimage/$',views.SaveProfile,name='testimage'),
    
=======
    url(r'^mobile_login/$',mobilefunctions.login,name='mobile_login'),
    url(r'^check_login/$',mobilefunctions.check_login,name='check_login'),
>>>>>>> 445bd947136d1b34093e0704878db473e79ba5ee

]


