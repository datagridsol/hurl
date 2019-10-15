
from django.db import models
from django.contrib.auth.models import User,Group
import datetime
# Create your models here.


class Language(models.Model):
    lang_name = models.CharField(max_length = 255)
    lang_code = models.CharField(max_length = 255)
    lang_code = models.CharField(max_length = 150)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    # class Meta:
    #     db_table='tbl_product'

class State(models.Model):
    state_name = models.CharField(max_length = 255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class District(models.Model):
    state_id=models.ForeignKey(State,on_delete=models.CASCADE)
    district_name = models.CharField(max_length = 255)
    district_id=models.IntegerField()
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class City(models.Model):
    city_name = models.CharField(max_length = 255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class UserProfile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id=models.IntegerField()
    user_type = models.ForeignKey(Group, on_delete=models.CASCADE)
    language= models.ForeignKey(Language, on_delete=models.CASCADE)
    aadhar_no=models.CharField(max_length=255)
    state=models.ForeignKey(State, on_delete=models.CASCADE)
    city=models.CharField(max_length=255,null=True, blank=True)
    district=models.ForeignKey(District, on_delete=models.CASCADE)
    pincode=models.IntegerField(null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    user_photo=models.ImageField(upload_to='media',blank=True)
    aadhar_card=models.ImageField(upload_to='media',blank=True)
    pan_card=models.ImageField(upload_to='media',blank=True)
    vote_id=models.ImageField(upload_to='media',blank=True)
    soil_card=models.ImageField(upload_to='media',blank=True)
    land_area=models.CharField(max_length=255,null=True, blank=True)
    otp=models.CharField(max_length=10,null=True, blank=True)
    fcm_id=models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class Product(models.Model):
    product_name = models.CharField(max_length = 255)
    product_code = models.CharField(max_length = 100)
    product_unit = models.CharField(max_length = 10)
    product_price = models.FloatField(null=True, blank=True)
    product_image = models.ImageField(upload_to='media',blank=True)
    total_price = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    # class Meta:
    #     db_table='tbl_product'

class Order(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user')
    total_price = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

    # class Meta:
    #     db_table='tbl_order'

class ManageContent(models.Model):
    title_eng=models.CharField(max_length=255)
    title_hnd=models.CharField(max_length=255)
    date=models.DateTimeField(default=datetime.datetime.now())
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    district=models.ForeignKey(District,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    contains_eng=models.TextField()
    contains_hnd=models.TextField()
    user_id_admin_id=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    feature_image=models.ImageField(upload_to='media',blank=True)


class Notification(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    district=models.ForeignKey(District,on_delete=models.CASCADE)
    message_eng=models.TextField()
    message_hnd=models.TextField()
    sms_status = models.IntegerField(default=0)
    push_status = models.IntegerField(default=0)
    sms_request=models.TextField()
    push_request=models.TextField()
    sms_response=models.TextField()
    push_response=models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=1)

class Support(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=255)
    query=models.CharField(max_length=255)
    created_at =models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class SupportReply(models.Model):
    support_id=models.ForeignKey(Support,on_delete=models.CASCADE)
    reply=models.TextField()
    user_id_admin_id=models.ForeignKey(User,on_delete=models.CASCADE)
    query=models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())


class Recharge(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth_recharge')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth_recharge')
    amount=models.CharField(max_length=255)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    transation_id=models.IntegerField()
    transation_request=models.TextField()
    transation_response=models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class MobileLang(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    lang_id=models.IntegerField()
    lang_key=models.CharField(max_length=255)
    lang_lab=models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class Scratch(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth')
    order_id =models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())


class OrderProductsDetail(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity =models.IntegerField()
    product_price = models.FloatField()
    product_total_price=models.FloatField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

class LoyaltyPoints(models.Model):
    loyalty_type= models.CharField(max_length=255)
    loyalty_point= models.IntegerField()
    conversion =models.CharField(max_length=255)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())


class UserLoyaltyPoints(models.Model):
    user_id_farmer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_user_auth_point')
    user_id_retailer_id= models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_user_auth_point')
    to_user_id=models.IntegerField()
    from_user_id=models.IntegerField()
    loyalty_type= models.CharField(max_length=255)
    loyalty_points_id= models.CharField(max_length=255)
    order_id =models.IntegerField()
    loyalty_point = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=1)



class Hotel(models.Model): 
    name = models.CharField(max_length=50) 
    hotel_Main_Img = models.ImageField(upload_to='media/') 