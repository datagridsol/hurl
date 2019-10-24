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
    name = forms.CharField(max_length = 100)
    picture = forms.ImageField() 

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


from django import forms 
class ProfileForm(forms.Form):
   name = forms.CharField(max_length = 100)
   picture = forms.ImageField()


class ManageContainForm(forms.ModelForm):
    class Meta:
        model = ManageContent
        fields = '__all__'

