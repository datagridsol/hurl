# dappx/forms.py
from django import forms
from hurlapp.models import UserProfile
from django.contrib.auth.models import User
from hurlapp.models import *
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
# class UserProfileInfoForm(forms.ModelForm):
#      class Meta():
#          model = UserProfileInfo
#          fields = ()

class HotelForm(forms.ModelForm): 
  
    class Meta: 
        model = Hotel 
        fields = ['name', 'hotel_Main_Img'] 

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfile
         fields = ('user_photo','aadhar_card')

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class ProductForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class OrderForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')
