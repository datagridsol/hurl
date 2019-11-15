# dappx/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render
from hurlapp.forms import UserForm,UserProfileInfoForm,HotelForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
import json
from hurlapp import models
from django.db.models import Q
from hurlapp.forms import ProfileForm
from hurlapp.models import UserProfile,Product,ManageContent
from hurlapp import forms
from hurl import settings
from django.utils.timezone import get_current_timezone
from datetime import datetime
import dateutil.parser
#from django.utils.encoding import smart_str, smart_unicode
import os
from operator import itemgetter
from datetime import timedelta
import io,csv
from pyfcm import FCMNotification
from django.db.models import Sum


def index(request):
    return render(request,'index.html')

def permission(request):
     return HttpResponseRedirect(reverse('user_login'))
@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def not_in_student_group(user):
    if user:
        return user.groups.filter(name='test2').count() == 0
    return False

#@permission_required("dappx.test1")
#@user_passes_test(not_in_student_group, login_url='/accounts/login/')
def register(request):
    registered = True
    #db_data=models.Test1.objects.all()
    data=['amol','jamdade']
    return render(request,'registration.html',
                          {'data':data})

@login_required
@csrf_exempt
def dashboard(request):
    total_farmer=0
    total_wholeseler=0
    total_retailer=0
    total_product=0
    total_order=0
    retailer_value=0
    order_value1=0
    start_date=''
    end_date=''
    retailer_loyalty_point=0
    if request.GET.get('searchDate'):
        searchDate=request.GET.get('searchDate')
        daterange= searchDate.split(" - ")
        start_date=daterange[0]
        
        newDate=datetime.strptime(start_date, '%d/%m/%Y')
        start_date=newDate.strftime("%Y-%m-%d")
        
        end_date1=str(daterange[1])
        newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
        end_date=newDate.strftime("%Y-%m-%d")
        total_farmer=UserProfile.objects.filter(user_type_id='3',created_at__range=(start_date, end_date)).count()
        total_wholeseler=UserProfile.objects.filter(user_type_id='4',created_at__range=(start_date, end_date)).count()
        total_retailer=UserProfile.objects.filter(user_type_id='2',created_at__range=(start_date, end_date)).count()
        total_product=Product.objects.filter(status='1',created_at__range=(start_date, end_date)).count()
        
        order_value=models.Order.objects.filter(status=1,created_at__range=(start_date, end_date)).aggregate(Sum('total_price'))
        if order_value['total_price__sum']:
            order_value1=order_value['total_price__sum']
        farmer_value=models.UserLoyaltyPoints.objects.filter(user_id_farmer_id__userprofile__user_type=3,created_at__range=(start_date, end_date)).aggregate(Sum('loyalty_point'))
        if farmer_value['loyalty_point__sum']==None:
            farmer_value1=0
        else:
            farmer_value1=farmer_value['loyalty_point__sum']

        
        retailer_value=models.UserLoyaltyPoints.objects.filter(user_id_retailer_id__userprofile__user_type=2,created_at__range=(start_date, end_date)).aggregate(Sum('loyalty_point'))
        if retailer_value['loyalty_point__sum']==None:
            retailer_value1=0
        else:
            retailer_value1=retailer_value['loyalty_point__sum']
        

    else:
        total_farmer=UserProfile.objects.filter(user_type_id='3').count()
        total_wholeseler=UserProfile.objects.filter(user_type_id='4').count()
        total_retailer=UserProfile.objects.filter(user_type_id='2').count()
        total_product=Product.objects.filter(status='1').count()
        order_value=models.Order.objects.filter(status=1).aggregate(Sum('total_price'))
        if order_value['total_price__sum']==None:
            order_value1=0
        else:
            order_value1=order_value['total_price__sum']

        farmer_value=models.UserLoyaltyPoints.objects.filter(user_id_farmer_id__userprofile__user_type=3).aggregate(Sum('loyalty_point'))
        if farmer_value['loyalty_point__sum']==None:
            farmer_value1=0
        else:
            farmer_value1=farmer_value['loyalty_point__sum']

        retailer_value=models.UserLoyaltyPoints.objects.filter(user_id_retailer_id__userprofile__user_type=2).aggregate(Sum('loyalty_point'))
        if retailer_value['loyalty_point__sum']==None:
            retailer_value1=0
        else:
            retailer_value1=retailer_value['loyalty_point__sum']

    data={'total_farmer':total_farmer,'total_wholeseler':total_wholeseler,"total_retailer":total_retailer,"total_product":total_product,"total_order":int(order_value1),"total_farmer_value":int(farmer_value1),"retailer_value":int(retailer_value1)}
    
    return render(request,'dashboard.html',{'data':data})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        data={'username':username,'password':password,"status":True}
        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            if user.is_active:
                user = authenticate(username=username, password=password)
                if user:  
                    login(request,user)
                    response=JsonResponse({'status':'success'})
                    if request.POST.get('remember'):
                        response.set_cookie('username', username)
                        response.set_cookie('password', password)
                    else:
                        response.delete_cookie('username')
                        response.delete_cookie('password')
                    return response
                else:
                    response=JsonResponse({'status':'error','msg':'Invalid login details'})
                    return response
            else:
                response=JsonResponse({'status':'error','msg':'Your account was inactive'})
                return response
        else:
            response=JsonResponse({'status':'error','msg':'Username Does not Exits'})
            return response
    
    else:
        username=''
        password=''
        if 'username' in request.COOKIES and 'password' in request.COOKIES:
            username = request.COOKIES['username']
            password = request.COOKIES['password']
        return render(request, 'login.html', {"username" : username,"password" : password})




@login_required
@csrf_exempt
def add_user(request):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
        if request.FILES.get('aadhar_card'):
            aadhar_card = request.FILES['aadhar_card']
        if request.FILES.get('pan_card'):
            pan_card = request.FILES['pan_card']
        if request.FILES.get('vote_id'):
            vote_id = request.FILES['vote_id']
        if request.FILES.get('soil_card'):
            soil_card = request.FILES['soil_card']
        if request.FILES.get('fertilizer_photo'):
            fertilizer_photo = request.FILES['fertilizer_photo']
        if request.FILES.get('gst_photo'):
            gst_photo = request.FILES['gst_photo']
        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id

        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number,created_at=datetime.now())
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'userprofile.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})
       

def add_state(request):
    states = ['JAMMU & KASHMIR','HIMACHAL PRADESH' ,'PUNJAB','CHANDIGARH','UTTARANCHAL','HARYANA','DELHI','RAJASTHAN','UTTAR PRADESH','BIHAR','SIKKIM','ARUNACHAL PRADESH','NAGALAND','MIZORAM','TRIPURA','MEGHALAYA','ASSAM','WEST BENGAL','JHARKHAND','CHHATTISGARH','MADHYA PRADESH','GUJARAT','DAMAN & DIU','DADRA & NAGAR HAVELI','MAHARASHTRA','ANDHRA PRADESH','KARNATAKA','LAKSHADWEEP','KERALA','TAMIL NADU','ANDAMAN & NICOBAR ISLANDS']
    for i in states:
        data = models.State.objects.create(state_name=i)
    data.save()    
    response = JsonResponse({'status':'success'})
    print(data)
    return response


@login_required
@csrf_exempt
def edit_user(request, pk):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    user_photo="/media/default/placeholder.png"
    aadhar_card="/media/default/placeholder.png"
    pan_card="/media/default/placeholder.png"
    vote_id="/media/default/placeholder.png"
    soil_card="/media/default/placeholder.png"
    gst_photo="/media/default/placeholder.png"
    fertilizer_photo="/media/default/placeholder.png"
    data={}
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_id=pk

    if request.method == 'POST':
        data={}
        #user_id = request.POST.get('user_id')
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        user_info_photo=list(models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card'))
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_profile = UserProfile.objects.get(user=user_id)

        if request.FILES.get('user_photo'):
            print("user_photo1",user_photo1)
            # if user_photo1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
            user_photo = request.FILES['user_photo']
            user_profile.user_photo = user_photo
            
        if request.FILES.get('aadhar_card'):
            # if aadhar_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
            aadhar_card = request.FILES['aadhar_card']
            user_profile.aadhar_card = aadhar_card
       
        if request.FILES.get('pan_card'):
            # if pan_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(pan_card1[0]))
            pan_card = request.FILES['pan_card']
            user_profile.pan_card = pan_card
        
        if request.FILES.get('vote_id'):
            # if vote_id1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(vote_id1[0]))
            vote_id = request.FILES['vote_id']
            user_profile.vote_id = vote_id
        
        

        if request.FILES.get('soil_card'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            soil_card = request.FILES['soil_card']
            user_profile.soil_card = soil_card

        if request.FILES.get('fertilizer_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            fertilizer_photo = request.FILES['fertilizer_photo']
            user_profile.fertilizer_photo = fertilizer_photo



        if request.FILES.get('gst_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            gst_photo = request.FILES['gst_photo']
            user_profile.gst_photo = gst_photo

        
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email,username=password)

        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
       
        user_profile.parent_id=0
        user_profile.language=langn_id
        user_profile.aadhar_no=aadhar_no
        user_profile.state=state
        user_profile.city_name=city_name
        user_profile.district=district
        user_profile.pincode=pincode
        user_profile.address=address
        user_profile.fms_id=fms_id
        user_profile.gst_number=gst_number
        user_profile.fertilizer_licence=fertilizer_licence
        user_profile.land_area=land_area
        user_profile.updated_at=datetime.now()
        user_profile.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id','gst_number','fertilizer_licence','fms_id','gst_photo','fertilizer_photo')
        for i in user_info:
            user_type=i[0],
            language=i[1]
            first_name=i[2]
            last_name=i[3]
            full_name=str(first_name)+" "+str(last_name)
            email=i[4]
            mobile_number=i[5]
            aadhar_no=i[6]
            state=i[7]
            city=i[8]
            district=i[9]
            pincode=i[10]
            address=i[11]
            if i[12]!= "":
                user_photo='/'+i[12]
            if i[13]!= "":
                aadhar_card='/'+i[13]
            if i[14]!= "":
                pan_card='/'+i[14]
            if i[15]!= "": 
                vote_id='/'+i[15]
            if i[16]!= "": 
                soil_card='/'+i[16] 
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            gst_number=i[22]
            fertilizer_licence=i[23]
            fms_id=i[24]
            if i[25]!= "": 
                gst_photo='/'+i[25]
            if i[26]!= "": 
                fertilizer_photo='/'+i[26]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':1,'name':'Thane'}],"user_id":user_id,"gst_number":gst_number,"fertilizer_licence":fertilizer_licence,"fms_id":fms_id,"gst_photo":gst_photo,"fertilizer_photo":fertilizer_photo}
        return render(request, 'edit_user.html',{'data':data})


@login_required
@csrf_exempt
def edit_retailer(request, pk):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    user_photo="/media/default/placeholder.png"
    aadhar_card="/media/default/placeholder.png"
    pan_card="/media/default/placeholder.png"
    vote_id="/media/default/placeholder.png"
    soil_card="/media/default/placeholder.png"
    gst_photo="/media/default/placeholder.png"
    fertilizer_photo="/media/default/placeholder.png"
    data={}
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_id=pk

    if request.method == 'POST':
        data={}
        #user_id = request.POST.get('user_id')
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        user_info_photo=models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card')
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_info_photo=list(models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card'))
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_profile = UserProfile.objects.get(user=user_id)

        if request.FILES.get('user_photo'):
            # if user_photo1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
            user_photo = request.FILES['user_photo']
            user_profile.user_photo = user_photo
            
        if request.FILES.get('aadhar_card'):
            # if aadhar_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
            aadhar_card = request.FILES['aadhar_card']
            user_profile.aadhar_card = aadhar_card
       
        if request.FILES.get('pan_card'):
            # if pan_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(pan_card1[0]))
            pan_card = request.FILES['pan_card']
            user_profile.pan_card = pan_card
        
        if request.FILES.get('vote_id'):
            # if vote_id1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(vote_id1[0]))
            vote_id = request.FILES['vote_id']
            user_profile.vote_id = vote_id
        
        if request.FILES.get('soil_card'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            soil_card = request.FILES['soil_card']
            user_profile.soil_card = soil_card

        if request.FILES.get('fertilizer_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            fertilizer_photo = request.FILES['fertilizer_photo']
            user_profile.fertilizer_photo = fertilizer_photo



        if request.FILES.get('gst_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            gst_photo = request.FILES['gst_photo']
            user_profile.gst_photo = gst_photo


        
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email,username=password)

        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
       
        user_profile.parent_id=0
        user_profile.language=langn_id
        user_profile.aadhar_no=aadhar_no
        user_profile.state=state
        user_profile.city_name=city_name
        user_profile.district=district
        user_profile.pincode=pincode
        user_profile.address=address
        user_profile.land_area=land_area
        user_profile.fms_id=fms_id
        user_profile.gst_number=gst_number
        user_profile.fertilizer_licence=fertilizer_licence
        user_profile.updated_at=datetime.now()
        user_profile.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id','gst_number','fertilizer_licence','fms_id','gst_photo','fertilizer_photo')
        for i in user_info:
            user_type=i[0],
            language=i[1]
            first_name=i[2]
            last_name=i[3]
            full_name=str(first_name)+" "+str(last_name)
            email=i[4]
            mobile_number=i[5]
            aadhar_no=i[6]
            state=i[7]
            city=i[8]
            district=i[9]
            pincode=i[10]
            address=i[11]
            if i[12]!= "":
                user_photo='/'+i[12]
            if i[13]!= "":
                aadhar_card='/'+i[13]
            if i[14]!= "":
                pan_card='/'+i[14]
            if i[15]!= "": 
                vote_id='/'+i[15]
            if i[16]!= "": 
                soil_card='/'+i[16] 
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            gst_number=i[22]
            fertilizer_licence=i[23]
            fms_id=i[24]
            if i[25]!= "": 
                gst_photo='/'+i[25]
            if i[26]!= "": 
                fertilizer_photo='/'+i[26]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':1,'name':'Thane'}],"user_id":user_id,"gst_number":gst_number,"fertilizer_licence":fertilizer_licence,"fms_id":fms_id,"gst_photo":gst_photo,"fertilizer_photo":fertilizer_photo}
        return render(request, 'edit_user.html',{'data':data})



@csrf_exempt
def user_status(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        user_details=User.objects.filter(id=user_id).values_list('first_name','last_name','username')
        full_name=user_details[0][0]+' '+user_details[0][1]
        mobile_number=user_details[0][2]
        sendapprove(full_name,'approved',mobile_number)
        response=JsonResponse({'status':'success','msg':'User Approved Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        user_details=User.objects.filter(id=user_id).values_list('first_name','last_name','username')
        full_name=user_details[0][0]+' '+user_details[0][1]
        mobile_number=user_details[0][2]
        sendapprove(full_name,'disapproved',mobile_number)
        response=JsonResponse({'status':'success','msg':'User Disapproved Successfuly'})
        return response

def get_username(request):
    username=request.POST.get('username')
    if User.objects.filter(username=username).exists():
        response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
        return response
    else:
        response=JsonResponse({'status':'success'})
        return response


def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name', 'lang_code')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],'code':i[2]}
        lang_data.append(case1)
    return lang_data


def get_group():
    group_data=[]

    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    data={}
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])

    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

        case = {'id': i[0], 'name': i[1]}
        group_data.append(case)
    return group_data
@csrf_exempt
def get_state():
    state_data=[]
    state_list=models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        state_data.append(case2)
    state_data=sorted(state_data, key=itemgetter('name'))
    return state_data

@csrf_exempt
def get_district(request):
    if request.method == 'POST':
        district_data=[]
        state_id=request.POST.get('state_id')
        district_list=models.District.objects.filter(state_id=state_id).values_list('id', 'district_name')
        for i in district_list:
            case2 = {'id': i[0], 'name': i[1]}
            district_data.append(case2)
            district_data=sorted(district_data, key=itemgetter('name'))
        response=JsonResponse({'status':'success','district_data':district_data})
        return response

def get_city():
    city_data=[]
    city_list=models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    return city_data



@login_required
@csrf_exempt
def get_manage_user(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(~Q(user='1')).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active').order_by('-created_at')
    for i in user_info:
        user_type=i[0]
        district=i[1]
        state=i[2]
        user_id=i[3]
        first_name=i[4]
        last_name=i[5]
        full_name=str(first_name)+" "+str(last_name)
        username=i[6]
        status=i[7]
        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-user-id="+str(user_id)+">Disapprove</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-user-id="+str(user_id)+">Approve</button></div>"
        count+=1
        if full_name=="Hurl Admin":
            pass
        else:
            data.append([count,str(user_type),str(full_name),str(username),str(district),str(state), str(status),str(btn),"<a href='/edit_user/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_user.html', {'data':(data)})



@csrf_exempt
def get_product(request):
    data=[]
    count=0
    product_image="/media/default/placeholder.png"
    product_info=models.Product.objects.all().values_list('product_image','product_name','product_code','product_unit','product_unit_name','product_price','status','id').order_by('-created_at')
    for i in product_info:
        if i[0]!= "":
            product_image='/'+i[0]
        product_name=i[1]
        product_code=i[2]
        product_unit=i[3]
        product_unit_name=i[4]
        product_price=i[5]
        status=i[6]
        product_id=i[7]
        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-product-id="+str(product_id)+">Deactive</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-product-id="+str(product_id)+">Active</button></div>"
        count+=1
        data.append([count,product_id,'<img src="'+str(product_image)+'"  width="70" height="50">',str(product_name),str(product_code),str(product_unit_name),str(product_price),status,btn,"<a href='/edit_product/"+str(product_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
#     return render(request, 'get_product.html', {'data':(data)})
    return render(request, 'get_product.html', {'data':(data)})



@csrf_exempt
def edit_product(request,pk):
    product_id=pk
    if request.method == 'POST':
        data={}
        product_image=''
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        product_unit = '0'
        product_unit_name = request.POST.get('product_unit_name')
        product_price = request.POST.get('product_price')
        if request.FILES.get('product_image'):
            product_image = request.FILES['product_image']

        product_data = Product.objects.get(id=product_id)
        product_data.product_name=product_name
        product_data.product_code=product_code
        product_data.product_unit=product_unit
        product_data.product_unit_name=product_unit_name
        product_data.product_price=product_price
        product_data.product_image=product_image
        product_data.updated_at=datetime.now()
        product_data.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        product_info=models.Product.objects.filter(id=product_id).values_list('product_image','product_name','product_code','product_unit','product_price','status','id','product_unit_name')
        
        data={'product_image':'/'+product_info[0][0],'product_name':product_info[0][1],'product_code':product_info[0][2],'product_unit':product_info[0][3],'product_price':product_info[0][4],'product_id':product_info[0][6],'product_unit_name':product_info[0][7]}
        
        return render(request, 'edit_product.html',{'data':data})

@login_required
@csrf_exempt
def edit_farmer(request, pk):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    user_photo="/media/default/placeholder.png"
    aadhar_card="/media/default/placeholder.png"
    pan_card="/media/default/placeholder.png"
    vote_id="/media/default/placeholder.png"
    soil_card="/media/default/placeholder.png"
    data={}
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_id=pk

    if request.method == 'POST':
        data={}
        #user_id = request.POST.get('user_id')
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        
        user_info_photo=models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card')
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_info_photo=list(models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card'))
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_profile = UserProfile.objects.get(user=user_id)

        if request.FILES.get('user_photo'):
            
            # if user_photo1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
            user_photo = request.FILES['user_photo']
            user_profile.user_photo = user_photo
            
        if request.FILES.get('aadhar_card'):
            # if aadhar_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
            aadhar_card = request.FILES['aadhar_card']
            user_profile.aadhar_card = aadhar_card
       
        if request.FILES.get('pan_card'):
            # if pan_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(pan_card1[0]))
            pan_card = request.FILES['pan_card']
            user_profile.pan_card = pan_card
        
        if request.FILES.get('vote_id'):
            # if vote_id1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(vote_id1[0]))
            vote_id = request.FILES['vote_id']
            user_profile.vote_id = vote_id
        
        if request.FILES.get('soil_card'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            soil_card = request.FILES['soil_card']
            user_profile.soil_card = soil_card
        
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email,username=password)

        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
       
        user_profile.parent_id=0
        user_profile.language=langn_id
        user_profile.aadhar_no=aadhar_no
        user_profile.state=state
        user_profile.city_name=city_name
        user_profile.district=district
        user_profile.pincode=pincode
        user_profile.address=address
        user_profile.land_area=land_area
        user_profile.updated_at=datetime.now()
        user_profile.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id')
        for i in user_info:
            user_type=i[0],
            language=i[1]
            first_name=i[2]
            last_name=i[3]
            full_name=str(first_name)+" "+str(last_name)
            email=i[4]
            mobile_number=i[5]
            aadhar_no=i[6]
            state=i[7]
            city=i[8]
            district=i[9]
            pincode=i[10]
            address=i[11]
            if i[12]!= "":
                user_photo='/'+i[12]
            if i[13]!= "":
                aadhar_card='/'+i[13]
            if i[14]!= "":
                pan_card='/'+i[14]
            if i[15]!= "": 
                vote_id='/'+i[15]
            if i[16]!= "": 
                soil_card='/'+i[16] 
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':1,'name':'Thane'}],"user_id":user_id}
        return render(request, 'edit_farmer.html',{'data':data})


# @login_required
# @csrf_exempt
# def edit_retailer(request, pk):
#     gr_no=[]
#     first_name=''
#     last_name=''
#     city_name=''
#     state=''
#     user_photo="/media/default/placeholder.png"
#     aadhar_card="/media/default/placeholder.png"
#     pan_card="/media/default/placeholder.png"
#     vote_id="/media/default/placeholder.png"
#     soil_card="/media/default/placeholder.png"
#     data={}
#     group_data=get_group()
#     lang_data=get_langauge()
#     state_data=get_state()
#     city_data=get_city()
#     user_id=pk

#     if request.method == 'POST':
#         data={}
#         #user_id = request.POST.get('user_id')
#         password = request.POST.get('mobile_number')
#         email = request.POST.get('email')
#         full_name = request.POST.get('name')
#         if (' ' in full_name) == True:
#             full_name_split=full_name.split(' ')
#             if len(full_name_split)==2:
#                 first_name=full_name_split[0]
#                 last_name=full_name_split[1]
#             if len(full_name_split)==3:
#                 first_name=full_name_split[0]
#                 last_name=full_name_split[2]
#         else:
#             first_name=full_name
#         langn_id=request.POST.get('language_id')
#         user_type = request.POST.get('user_type')
#         aadhar_no=request.POST.get('aadhar_no')
#         state=request.POST.get('state')
#         city=request.POST.get('city')
#         district=request.POST.get('district')
#         pincode=request.POST.get('pincode')
#         address=request.POST.get('address')
#         fms_id=request.POST.get('fms_id')
#         fertilizer_licence=request.POST.get('fertilizer_licence')
#         gst_number=request.POST.get('gst_number')
#         user_info_photo=list(models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card'))
#         for i in user_info_photo:
#             user_photo1=i[0],
#             aadhar_card1=i[1]
#             pan_card1=i[2]
#             vote_id1=i[3]
#             soil_card1=i[4]
#         user_profile = UserProfile.objects.get(user=user_id)

#         if request.FILES.get('user_photo'):
#             print("user_photo1",user_photo1)
#             # if user_photo1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
#             user_photo = request.FILES['user_photo']
#             user_profile.user_photo = user_photo
            
#         if request.FILES.get('aadhar_card'):
#             # if aadhar_card1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
#             aadhar_card = request.FILES['aadhar_card']
#             print("sssssss",aadhar_card)
#             user_profile.aadhar_card = aadhar_card
       
#         if request.FILES.get('pan_card'):
#             # if pan_card1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(pan_card1[0]))
#             pan_card = request.FILES['pan_card']
#             user_profile.pan_card = pan_card
        
#         if request.FILES.get('vote_id'):
#             # if vote_id1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(vote_id1[0]))
#             vote_id = request.FILES['vote_id']
#             user_profile.vote_id = vote_id
        
#         if request.FILES.get('soil_card'):
#             # if soil_card1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
#             soil_card = request.FILES['soil_card']
#             user_profile.soil_card = soil_card
        
#         if request.FILES.get('fertilizer_photo'):
#             # if soil_card1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
#             fertilizer_photo = request.FILES['fertilizer_photo']
#             user_profile.fertilizer_photo = fertilizer_photo



#         if request.FILES.get('gst_photo'):
#             # if soil_card1:
#             #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
#             gst_photo = request.FILES['gst_photo']
#             user_profile.gst_photo = gst_photo

#         land_area=request.POST.get('land_area')

#         models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email)

#         langn_id=models.Language.objects.get(id=langn_id)
#         state=models.State.objects.get(id=state)
#         district=models.District.objects.get(id=district)
#         if city:
#             if models.City.objects.filter(city_name=city).exists():
#                 city_name=city
#             else:
#                 new_city = models.City.objects.create(city_name =city,status=1)
#                 new_city.save()
#                 city_name=new_city.city_name
       
#         user_profile.parent_id=0
#         user_profile.language=langn_id
#         user_profile.aadhar_no=aadhar_no
#         user_profile.state=state
#         user_profile.city_name=city_name
#         user_profile.district=district
#         user_profile.pincode=pincode
#         user_profile.address=address
#         user_profile.land_area=land_area
#         user_profile.fms_id=fms_id
#         user_profile.gst_number=gst_number
#         user_profile.fertilizer_licence=fertilizer_licence
#         user_profile.save()
#         response=JsonResponse({'status':'success'})
#         return response
#     else:
#         user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id','gst_number','fertilizer_licence','fms_id','gst_photo','fertilizer_photo')
#         for i in user_info:
#             user_type=i[0],
#             language=i[1]
#             first_name=i[2]
#             last_name=i[3]
#             full_name=str(first_name)+" "+str(last_name)
#             email=i[4]
#             mobile_number=i[5]
#             aadhar_no=i[6]
#             state=i[7]
#             city=i[8]
#             district=i[9]
#             pincode=i[10]
#             address=i[11]
#             if i[12]!= "":
#                 user_photo='/'+i[12]
#             if i[13]!= "":
#                 aadhar_card='/'+i[13]
#             if i[14]!= "":
#                 pan_card='/'+i[14]
#             if i[15]!= "": 
#                 vote_id='/'+i[15]
#             if i[16]!= "": 
#                 soil_card='/'+i[16] 
#             land_area=i[17]
#             group_id=i[18]
#             lang_id=i[19]
#             state_id=i[20]
#             district_id=i[21]
#             gst_number=i[22]
#             fertilizer_licence=i[23]
#             fms_id=i[24]
#             if i[25]!= "": 
#                 gst_photo='/'+i[25]
#             if i[26]!= "": 
#                 fertilizer_photo='/'+i[26]
#             user_type={"name":user_type[0],'id':group_id}
#             language={"name":language,'id':lang_id}
#             state={"name":state,'id':state_id}
#             district={"name":district,'id':district_id}
#             print("user_photo",user_photo)
#             data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':1,'name':'Thane'}],"user_id":user_id,"fms_id":fms_id,"gst_photo":gst_photo,"fertilizer_photo":fertilizer_photo}
#         return render(request, 'edit_retailer.html',{'data':data})


@login_required
@csrf_exempt
def edit_wholesaler(request, pk):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    user_photo="/media/default/placeholder.png"
    aadhar_card="/media/default/placeholder.png"
    pan_card="/media/default/placeholder.png"
    vote_id="/media/default/placeholder.png"
    soil_card="/media/default/placeholder.png"
    gst_photo="/media/default/placeholder.png"
    fertilizer_photo="/media/default/placeholder.png"

    data={}
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_id=pk

    if request.method == 'POST':
        data={}
        #user_id = request.POST.get('user_id')
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        user_info_photo=models.UserProfile.objects.filter(user=pk).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card')
        for i in user_info_photo:
            user_photo1=i[0],
            aadhar_card1=i[1]
            pan_card1=i[2]
            vote_id1=i[3]
            soil_card1=i[4]
        user_profile = UserProfile.objects.get(user=user_id)

        if request.FILES.get('user_photo'):
           
            # if user_photo1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
            user_photo = request.FILES['user_photo']
            user_profile.user_photo = user_photo
            
        if request.FILES.get('aadhar_card'):
            # if aadhar_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
            aadhar_card = request.FILES['aadhar_card']
           
            user_profile.aadhar_card = aadhar_card
       
        if request.FILES.get('pan_card'):
            # if pan_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(pan_card1[0]))
            pan_card = request.FILES['pan_card']
            user_profile.pan_card = pan_card
        
        if request.FILES.get('vote_id'):
            # if vote_id1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(vote_id1[0]))
            vote_id = request.FILES['vote_id']
            user_profile.vote_id = vote_id
        
        if request.FILES.get('soil_card'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            soil_card = request.FILES['soil_card']
            user_profile.soil_card = soil_cardser_profile.soil_card = soil_card
        
        if request.FILES.get('fertilizer_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            fertilizer_photo = request.FILES['fertilizer_photo']
            user_profile.fertilizer_photo = fertilizer_photo



        if request.FILES.get('gst_photo'):
            # if soil_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(soil_card1[0]))
            gst_photo = request.FILES['gst_photo']
            user_profile.gst_photo = gst_photo

        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email,username=password)

        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
       
        user_profile.parent_id=0
        user_profile.language=langn_id
        user_profile.aadhar_no=aadhar_no
        user_profile.state=state
        user_profile.city_name=city_name
        user_profile.district=district
        user_profile.pincode=pincode
        user_profile.address=address
        user_profile.land_area=land_area
        user_profile.fms_id=fms_id
        user_profile.gst_number=gst_number
        user_profile.fertilizer_licence=fertilizer_licence
        user_profile.updated_at=datetime.now()
        user_profile.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id','gst_number','fertilizer_licence','fms_id','gst_photo','fertilizer_photo')
        for i in user_info:
            user_type=i[0],
            language=i[1]
            first_name=i[2]
            last_name=i[3]
            full_name=str(first_name)+" "+str(last_name)
            email=i[4]
            mobile_number=i[5]
            aadhar_no=i[6]
            state=i[7]
            city=i[8]
            district=i[9]
            pincode=i[10]
            address=i[11]
            if i[12]!= "":
                user_photo='/'+i[12]
            if i[13]!= "":
                aadhar_card='/'+i[13]
            if i[14]!= "":
                pan_card='/'+i[14]
            if i[15]!= "": 
                vote_id='/'+i[15]
            if i[16]!= "": 
                soil_card='/'+i[16] 
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            gst_number=i[22]
            fertilizer_licence=i[23]
            fms_id=i[24]
            if i[25]!= "": 
                gst_photo='/'+i[25]
            if i[26]!= "": 
                fertilizer_photo='/'+i[26]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
           
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':1,'name':'Thane'}],"user_id":user_id,"gst_number":gst_number,"fertilizer_licence":fertilizer_licence,"fms_id":fms_id,"gst_photo":gst_photo,"fertilizer_photo":fertilizer_photo}
        return render(request, 'edit_wholesaler.html',{'data':data})


def get_username(request):
    username=request.POST.get('username')
    if User.objects.filter(username=username).exists():
        response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
        return response
    else:
        response=JsonResponse({'status':'success'})
        return response


def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name', 'lang_code')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],'code':i[2]}
        lang_data.append(case1)
    return lang_data


def get_group():
    group_data=[]
    gr_no=[]
    user_type=Group.objects.filter(~Q(id=1)).values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
        case = {'id': i[0], 'name': i[1]}
        group_data.append(case)
    return group_data
@csrf_exempt
def get_state():
    state_data=[]
    state_list=models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name':i[1].capitalize()}
        state_data.append(case2)
    state_data=sorted(state_data, key=itemgetter('name'))
    return state_data

@csrf_exempt
def get_district(request):
    if request.method == 'POST':
        district_data=[]
        state_id=request.POST.get('state_id')
        district_list=models.District.objects.filter(state_id=state_id).values_list('id', 'district_name')
        for i in district_list:
            case2 = {'id': i[0], 'name': i[1]}
            district_data.append(case2)
            district_data=sorted(district_data, key=itemgetter('name'))
        response=JsonResponse({'status':'success','district_data':district_data})
        return response

def get_city():
    city_data=[]
    city_list=models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    return city_data

def search_city(request):
    
    #print(request.GET)
    city_name=request.GET.get('query')
    #print(city_name)
    city_list=models.City.objects.filter(city_name__startswith=city_name).values_list('city_name')
    
    results = []
    for i in city_list:
        results.append(i[0])
    
    mimetype = 'application/json'
    response=HttpResponse(json.dumps(results),mimetype)
    print(response)

    return response

def product_unit(request):
    
    #print(request.GET)
    unit_name=request.GET.get('query')
    #print(city_name)
    city_list=models.ProductUnit.objects.filter(unit_name__startswith=unit_name).values_list('unit_name')
    
    results = []
    for i in city_list:
        results.append(i[0])
    
    mimetype = 'application/json'
    response=HttpResponse(json.dumps(results),mimetype)
    print(response)

    return response


@csrf_exempt
def add_product(request):
    
    if request.method == 'POST':
        data={}
        product_image=''
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        product_unit = '0'
        product_unit_name = request.POST.get('product_unit_name')
        if product_unit_name:
            if models.ProductUnit.objects.filter(unit_name=product_unit_name).exists():
                product_unit_name=product_unit_name
            else:
                new_product_unit = models.ProductUnit.objects.create(unit_name =product_unit_name,status=1)
                new_product_unit.save()
                product_unit_name=new_product_unit.unit_name
        product_price = request.POST.get('product_price')
        if request.FILES.get('product_image'):
            product_image = request.FILES['product_image']

        product = models.Product.objects.create(product_name=product_name,product_code=product_code,product_unit=product_unit,product_unit_name=product_unit_name,product_price=product_price,product_image=product_image)
        product.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'product.html', {})



@login_required
@csrf_exempt
def add_retailer(request):
    gr_no=[]

    first_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

    if request.method == 'POST':
       
        data={}
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type =2
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
        if request.FILES.get('aadhar_card'):
            aadhar_card = request.FILES['aadhar_card']
        if request.FILES.get('pan_card'):
            pan_card = request.FILES['pan_card']
        if request.FILES.get('vote_id'):
            vote_id = request.FILES['vote_id']
        if request.FILES.get('soil_card'):
            soil_card = request.FILES['soil_card']
        if request.FILES.get('fertilizer_photo'):
            fertilizer_photo = request.FILES['fertilizer_photo']
        if request.FILES.get('gst_photo'):
            gst_photo = request.FILES['gst_photo']

        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        #MyProfileForm = forms.ProfileForm()
        return render(request, 'add_retailer.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@login_required
@csrf_exempt
def get_retailer(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=2).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active').order_by('-created_at')
    for i in user_info:
        user_type=i[0]
        district=i[1]
        state=i[2]
        user_id=i[3]
        first_name=i[4]
        last_name=i[5]
        full_name=str(first_name)+" "+str(last_name)
        username=i[6]
        status=i[7]

        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-user-id="+str(user_id)+">Deactive</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-user-id="+str(user_id)+">Active</button></div>"

        count+=1
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),btn,"<a href='/edit_retailer/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a> | <a class='btn' href='/loyalty_retailer/"+str(user_id)+"'><i class='fas fa-gift'></i> Loyalty Points</a>"])
    return render(request, 'manage_retailer.html', {'data':(data)})


@login_required
@csrf_exempt
def add_farmer(request):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type = 3
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
        if request.FILES.get('aadhar_card'):
            aadhar_card = request.FILES['aadhar_card']
        if request.FILES.get('pan_card'):
            pan_card = request.FILES['pan_card']
        if request.FILES.get('vote_id'):
            vote_id = request.FILES['vote_id']
        if request.FILES.get('soil_card'):
            soil_card = request.FILES['soil_card']
        if request.FILES.get('fertilizer_photo'):
            fertilizer_photo = request.FILES['fertilizer_photo']
        if request.FILES.get('gst_photo'):
            gst_photo = request.FILES['gst_photo']
        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id

        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number,created_at=datetime.now())
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_farmer.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@login_required
@csrf_exempt
def get_farmer(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=3).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active').order_by('-created_at')
    for i in user_info:
        user_type=i[0]
        district=i[1]
        state=i[2]
        user_id=i[3]
        first_name=i[4]
        last_name=i[5]
        full_name=str(first_name)+" "+str(last_name)
        username=i[6]
        status=i[7]
	
        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-user-id="+str(user_id)+">Deactive</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-user-id="+str(user_id)+">Active</button></div>"

        count+=1
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),btn,"<a href='/edit_farmer/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/farmer_view/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_farmer.html', {'data':(data)})

@login_required
@csrf_exempt
def add_wholesaler(request):
    gr_no=[]

    first_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    pan_card=''
    vote_id=''
    soil_card=''
    fertilizer_photo=''
    gst_photo=''
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        email = request.POST.get('email')
        full_name = request.POST.get('name')
        if (' ' in full_name) == True:
            full_name_split=full_name.split(' ')
            if len(full_name_split)==2:
                first_name=full_name_split[0]
                last_name=full_name_split[1]
            if len(full_name_split)==3:
                first_name=full_name_split[0]
                last_name=full_name_split[2]
        else:
            first_name=full_name
        langn_id=request.POST.get('language_id')
        user_type =4
        print("user_typeuser_type",user_type)
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        fms_id=request.POST.get('fms_id')
        fertilizer_licence=request.POST.get('fertilizer_licence')
        gst_number=request.POST.get('gst_number')
        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
        if request.FILES.get('aadhar_card'):
            aadhar_card = request.FILES['aadhar_card']
        if request.FILES.get('pan_card'):
            pan_card = request.FILES['pan_card']
        if request.FILES.get('vote_id'):
            vote_id = request.FILES['vote_id']
        if request.FILES.get('soil_card'):
            soil_card = request.FILES['soil_card']
        if request.FILES.get('fertilizer_photo'):
            fertilizer_photo = request.FILES['fertilizer_photo']
        if request.FILES.get('gst_photo'):
            gst_photo = request.FILES['gst_photo']

        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number,created_at=datetime.now())
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_wholesaler.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})


@login_required
@csrf_exempt
def get_wholesaler(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=4).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active').order_by('-created_at')
    for i in user_info:
        user_type=i[0]
        district=i[1]
        state=i[2]
        user_id=i[3]
        first_name=i[4]
        last_name=i[5]
        full_name=str(first_name)+" "+str(last_name)
        username=i[6]
        status=i[7]
        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-user-id="+str(user_id)+">Deactive</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-user-id="+str(user_id)+">Active</button></div>"

        count+=1
        
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),btn,"<a href='/edit_wholesaler/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_wholesaler.html', {'data':(data)})



@login_required
@csrf_exempt
def get_order(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.Order.objects.all().values_list('user_id_farmer_id__first_name','user_id_farmer_id__last_name','user_id_retailer_id__first_name','user_id_retailer_id__last_name','created_at','user_id_farmer_id__userprofile__state__state_name','user_id_farmer_id__userprofile__district__district_name','total_price','id').order_by('-created_at')
    for i in user_info:
        first_name=i[0]
        last_name=i[1]
        full_name=str(first_name)+" "+str(last_name)

        first_name_retailer=i[2]
        last_name_retailer=i[3]
        full_name_retailer=str(first_name_retailer)+" "+str(last_name_retailer)

        created_at=i[4]
	#end_time = datetime.datetime.utcnow().replace(microsecond =0)
        formatedDate1= (created_at + timedelta(hours = 5,minutes = 30))
        formatedDate = formatedDate1.strftime("%d-%m-%Y %H:%M:%S")
        state=i[5]
        district=i[6]
        amount=i[7]
        id=i[8]

        count+=1
        data.append([count,id,str(full_name),str(full_name_retailer),str(formatedDate),str(state),str(district),str(amount),"<a class='btn' href='/order_details/"+str(id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_orders.html', {'data':(data)})

@csrf_exempt
def addOrder(request):
    if request.user.groups.filter(name="admin").exists():
        print("in")
    else:
        print ("out")
    print("Add USer")
    if request.method == 'POST':
        print("POST")
        data={}
        product_name = request.POST.get('product_name')
        product_unit = request.POST.get('product_unit')

        print("values",product_name,product_unit)
        user = models.Product.objects.create(product_name=product_name,product_unit=product_unit,created_at=datetime.now())
        user.save()
        #remember_me = request.POST.get('remember_me')
        #print("Insideeee",remember_me)
        data={'product_name':product_name,'product_unit':product_unit,"status":True}
        return render(request, 'order.html', {})

    else:
        #return render(request, 'login.html', {})
        return render(request, 'order.html', {})


@csrf_exempt
def order_details(request,pk):
    data_prod=[]
    count=0
    order_info=models.Order.objects.filter(id=pk).values_list('user_id_farmer_id__first_name','user_id_farmer_id__last_name','user_id_retailer_id__first_name','user_id_retailer_id__last_name','created_at','user_id_farmer_id__userprofile__state__state_name','user_id_farmer_id__userprofile__district__district_name','total_price','id','user_id_retailer_id__userprofile__address','user_id_farmer_id__username')

    first_name=order_info[0][0]
    last_name=order_info[0][1]
    full_name=str(first_name)+" "+str(last_name)

    first_name_retailer=order_info[0][2]
    last_name_retailer=order_info[0][3]
    full_name_retailer=str(first_name_retailer)+" "+str(last_name_retailer)

    created_at=order_info[0][4]
    formatedDate = created_at.strftime("%d-%m-%Y %H:%M:%S")
    state=order_info[0][5]
    district=order_info[0][6]
    amount=order_info[0][7]
    id=order_info[0][8]
    address=order_info[0][9]
    phone=order_info[0][10]

    product_image="media/default/placeholder.png"
    order_details=models.OrderProductsDetail.objects.filter(order_id=id).values_list('product_id','product_price','product_quantity','product_total_price','product__product_name','product__product_image','product__product_unit_name')
    
    for i in order_details:
        product_id=i[0]
        product_price=i[1]
        product_quantity=i[2]
        product_total_price=i[3]
        product_name=i[4]
        if i[5]!= "":
            product_image=i[5]
        product_unit_name=i[6]
        count+=1
        data_prod.append([count,product_id,'<img src="/'+str(product_image)+'"  width="70" height="50">',str(product_name),str(product_quantity)+' '+str(product_unit_name),str(product_price),str(product_total_price)])
    
    data={'full_name':full_name,'full_name_retailer':full_name_retailer,'created_at':formatedDate,'state':state,'district':district,'amount':amount,'id':id,'address':address,'phone':phone,'data_prod':data_prod}
    
    return render(request, 'order-details.html',{'data':data})

# Create your views here. 
def hotel_image_view(request): 
  
    if request.method == 'POST': 
        form = HotelForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = HotelForm() 
    return render(request, 'userprofile.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfuly uploaded')



# from hurlapp.forms import ProfileForm
# from hurlapp.models import Hotel
# import os 
# def SaveProfile(request):
#     saved = False 
#     if request.method == "POST":
#       print("request.POST",request.POST)
#       print("request.POST",request.FILES)
#       MyProfileForm = ProfileForm(request.POST, request.FILES)      
#       if MyProfileForm.is_valid():
#          print("valid")
#          profile = models.Hotel()
#          profile.name = MyProfileForm.cleaned_data["name"]
#          profile.hotel_Main_Img = MyProfileForm.cleaned_data["picture"]
#          profile.save()
#          saved = True
#          response=JsonResponse({'status':'success'})
#          return response
#       else:
#           print("not Valid")

#     else:
#        MyProfileForm = forms.ProfileForm()
#     return render(request, 'profile.html', {"group_data":get_group()})

@csrf_exempt
def check_user_mobile(request):
    
    mobile_number=request.POST.get('mobile_number')
    user_id=request.POST.get('user_id')
    if mobile_number:
        if user_id:
            if User.objects.filter(~Q(id = user_id),username=mobile_number).exists():
                res="false"
            else:
                res="true"
        else:
            if User.objects.filter(username=mobile_number).exists():
                res="false"
            else:
                res="true"
    else:
        res="false"
    return HttpResponse(res)

@csrf_exempt
def check_aadhar_card(request):
    
    aadhar_no=request.POST.get('aadhar_no')
    user_id=request.POST.get('user_id')
    if aadhar_no:
        if user_id:
            if UserProfile.objects.filter(~Q(user = user_id),aadhar_no=aadhar_no).exists():
                res="false"
            else:
                res="true"
        else:
            if UserProfile.objects.filter(aadhar_no=aadhar_no).exists():
                res="false"
            else:
                res="true"
    else:
        res="false"
    return HttpResponse(res)

@login_required
@csrf_exempt
def user_profile(request, pk):
        user_photo="/media/default/placeholder.png"
        aadhar_card="/media/default/placeholder.png"
        pan_card="/media/default/placeholder.png"
        vote_id="/media/default/placeholder.png"
        soil_card="/media/default/placeholder.png"
        user_info=models.UserProfile.objects.filter(user=pk).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id')
        for i in user_info:
            user_type=i[0],
            language=i[1]
            first_name=i[2]
            last_name=i[3]
            full_name=str(first_name)+" "+str(last_name)
            email=i[4]
            mobile_number=i[5]
            aadhar_no=i[6]
            state=i[7]
            city=i[8]
            district=i[9]
            pincode=i[10]
            address=i[11]
            if i[12]!= "":
                user_photo='/'+i[12]
            if i[13]!= "":
                aadhar_card='/'+i[13]
            if i[14]!= "":
                pan_card='/'+i[14]
            if i[15]!= "": 
                vote_id='/'+i[15]
            if i[16]!= "": 
                soil_card='/'+i[16]
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"pan_card":pan_card,"vote_id":vote_id,"aadhar_card":aadhar_card,"soil_card":soil_card,"land_area":land_area}
            
        return render(request, 'user_profile.html',{'data':data})

@csrf_exempt
def product_status(request):
    status=request.POST.get('status')
    product_id=request.POST.get('product_id')
    if status=="Deactive":
        user_details=Product.objects.get(id=product_id)
        user_details.status=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Product Approved Successfuly'})
        return response
    else:
        user_details=Product.objects.get(id=product_id)
        user_details.status=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Product Disapproved Successfuly'})
        return response


@csrf_exempt
def get_content(request):
    data=[]
    count=0
    feature_image="/media/default/placeholder.png"
    #product_info=models.ManageContent.objects.all().values_list('title_eng','title_hnd','date','status','feature_image','district_id','state_id','group_id','id')
    user_info=models.ManageContent.objects.all().values_list('title_eng','title_hnd','date','status','feature_image','district_id','state_id','group_id','id').order_by('-created_at')
    for i in user_info:
        if i[4]!= "":
            feature_image='/'+i[4]
        title_eng=i[0]
        title_hnd=i[1]
        district=i[5]
        if district != 0:
            district=models.District.objects.get(id=district)
        else:
            district="-"
        state=i[6]
        if state != 0:
            state=models.State.objects.get(id=state)
        else:
            state="-"
        status=i[3]
        group=i[7]
        grouTxt=''
        if(group):
            Arr=group.split(',')
            for gid in Arr:
                grouTxt=str(Group.objects.get(id=gid))+','+str(grouTxt)

        id=i[8]
        if status:
            status="Active"
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-content-id="+str(id)+">Deactive</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-content-id="+str(id)+">Active</button></div>"
        count+=1
        data.append([count,'<img src="'+str(feature_image)+'"  width="70" height="50">',str(title_eng),str(district),str(state),str(grouTxt[:-1]),status,btn,"<a href='/edit_content/"+str(id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
    return render(request, 'manage_content.html', {'data':(data)})


@csrf_exempt
def add_content(request):
    lang_data=get_langauge()
    state_data=get_state()
    if request.method == 'POST':
        data={}
        
        feature_image=''
        group_id = ','.join(request.POST.getlist('user_type[]'))
        title_eng = request.POST.get('title_eng')
        title_hnd = request.POST.get('title_hnd')
        date = request.POST.get('datetime')+':00'
        dt = dateutil.parser.parse(date)
        contains_eng = request.POST.get('content_eng')
        contains_hnd = request.POST.get('content_hnd')
        status = '1'
        district_id = request.POST.get('district')
        if district_id == '':
           district_id=0
        else:
           district_id=district_id  
        state_id = request.POST.get('state')
        if state_id == '':
           state_id=0
        else:
           state_id=state_id
        user_id_admin_id_id = request.user.id

        if request.FILES.get('feature_image'):
            feature_image = request.FILES['feature_image']
        

        Content = models.ManageContent.objects.create(title_eng=title_eng,title_hnd=title_hnd,date=dt,contains_eng=contains_eng,contains_hnd=contains_hnd,feature_image=feature_image,status=status,district_id=district_id,group_id=group_id,state_id=state_id,user_id_admin_id_id=user_id_admin_id_id,created_at=datetime.now())
        Content.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        data={'languages':lang_data,'state_data':state_data}
        return render(request, 'add-content.html', {'data':data})

@csrf_exempt
def content_status(request):
    status=request.POST.get('status')
    content_id=request.POST.get('content_id')
    if status=="Deactive":
        user_details=ManageContent.objects.get(id=content_id)
        user_details.status=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Content Approved Successfuly'})
        return response
    else:
        user_details=ManageContent.objects.get(id=content_id)
        user_details.status=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Content Disapproved Successfuly'})
        return response


@csrf_exempt
def edit_content(request,pk):
    lang_data=get_langauge()
    state_data=get_state()
    content_id=pk
    if request.method == 'POST':
        data={}
        
        feature_image=''
        group_id = ','.join(request.POST.getlist('user_type[]'))
        title_eng = request.POST.get('title_eng')
        title_hnd = request.POST.get('title_hnd')
        date = request.POST.get('datetime')+':00'
        dt = dateutil.parser.parse(date)
        contains_eng = request.POST.get('content_eng')
        contains_hnd = request.POST.get('content_hnd')

        district_id = request.POST.get('district')
        if district_id == '':
           district_id=0
        else:
           district_id=district_id  
        state_id = request.POST.get('state')
        if state_id == '':
           state_id=0
        else:
           state_id=state_id
        user_id_admin_id_id = request.user.id

        user_info_photo=list(models.ManageContent.objects.filter(id=pk).values_list('feature_image'))
        for i in user_info_photo:
            feature_image=i[0]
            

        if request.FILES.get('feature_image'):
            feature_image=request.FILES.get('feature_image')
            # if feature_image:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(feature_image))
           	
        #Content = models.ManageContent.objects.create(title_eng=title_eng,title_hnd=title_hnd,date=dt,contains_eng=contains_eng,contains_hnd=contains_hnd,feature_image=feature_image,status=status,district_id=district_id,group_id=group_id,state_id=state_id,user_id_admin_id_id=user_id_admin_id_id)


        content = ManageContent.objects.get(id=content_id)
        content.title_eng=title_eng
        content.title_hnd=title_hnd
        content.date=dt
        content.contains_eng=contains_eng
        content.contains_hnd=contains_hnd
        content.feature_image=feature_image
        content.district_id=district_id
        content.group_id=group_id
        content.state_id=state_id
        content.user_id_admin_id_id=user_id_admin_id_id
        content.updated_at=datetime.now()

        content.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        content_info=models.ManageContent.objects.filter(id=content_id).values_list('title_eng','title_hnd','date','feature_image','district_id','state_id','group_id','id','contains_eng','contains_hnd')
        
        data={'feature_image':'/'+content_info[0][3],'title_eng':content_info[0][0],'title_hnd':content_info[0][1],'date':content_info[0][2],'district':content_info[0][4],'state':content_info[0][5],'group_id':content_info[0][6],'content_id':content_info[0][7],'languages':lang_data,'state_data':state_data,'contains_eng':content_info[0][8],'contains_hnd':content_info[0][9]}
        print(data)
        return render(request, 'edit-content.html',{'data':data})

@csrf_exempt
def get_support(request):
    data=[]
    count=0
    
    user_info=models.Support.objects.all().values_list('id','query','subject','created_at','user__first_name','user__last_name','user__groups__name').order_by('-updated_at')
   
    for i in user_info:
        id=i[0]
        query=i[1]
        subject=i[2]
        created_at=i[3]
        formatedDate = created_at.strftime("%d-%m-%Y %H:%M:%S")
        first_name=i[4]
        last_name=i[5]
        user_type=i[6]

        count+=1
        data.append([count,str(first_name)+' '+str(last_name),str(user_type),str(subject),str(formatedDate),"<a href='/view_support/"+str(id)+"' class='btn'><i class='fas fa-eye'></i> Reply Now</a>"])
    return render(request, 'manage_support.html', {'data':(data)})

@csrf_exempt
def view_support(request,pk):
    count=0
    data_reply=[]

    if request.method == 'POST':
       
        reply = request.POST.get('message')
        user_id_admin_id_id = request.user.id
        
        support = models.SupportReply.objects.create(reply=reply,support_id_id=pk,user_id_admin_id_id=user_id_admin_id_id)
        support.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        user_info=models.Support.objects.filter(id=pk).values_list('id','query','subject','created_at','user__first_name','user__last_name','user__groups__name').order_by('created_at')
        id=user_info[0][0]
        query=user_info[0][1]
        subject=user_info[0][2]
        created_at=user_info[0][3]
        formatedDate = created_at.strftime("%d-%m-%Y %H:%M:%S")
        first_name=user_info[0][4]
        last_name=user_info[0][5]
        user_type=user_info[0][6]

        user_chats=models.SupportReply.objects.filter(support_id_id=pk).values_list('id','query','reply','created_at','user_id_admin_id').order_by('id')
        for i in user_chats:
            chat_id=i[0]
            chat_query=i[1]
            reply=i[2]
            chat_created_at=i[3]
            chat_formatedDate = chat_created_at.strftime("%d/%m/%Y %H:%M")
            user_id_admin_id=i[4]

            count+=1
            data_reply.append({'count':count,'chat_id':chat_id,'chat_query':chat_query,'reply':reply,'created_at':chat_formatedDate,'user_id_admin_id':user_id_admin_id})


        data={'full_name':str(first_name)+' '+str(last_name),'id':id,'subject':subject,'date':formatedDate,'user_type':user_type,'data_reply':data_reply}
        return render(request, 'view_support.html', {'data':data})


# @csrf_exempt
# def get_reports(request):
#     data=[]
#     count=0
#     state_data=get_state()
#     user_info=models.Order.objects.all().values_list('id','user_id_retailer_id__first_name','user_id_retailer_id__username','user_id_farmer_id__first_name','user_id_farmer_id__username','created_at','total_price','user_id_retailer_id__last_name','user_id_farmer_id__last_name').order_by('-updated_at')
#     for i in user_info:
#         id=i[0]
#         retailer_first_name=i[1]
#         retailer_username=i[2]
#         farmer__first_name=i[3]
#         farmer_username=i[4]
#         created_at=i[5]
#         total_price=i[6]
#         retailer_last_name=i[7]
#         farmer_last_name=i[8]
#         formatedDate = created_at.strftime("%d-%m-%Y")

#         count+=1
#         data.append([count,str(retailer_first_name)+' '+str(retailer_last_name),str(retailer_username),str(farmer__first_name)+' '+str(farmer_last_name),str(farmer_username),str(formatedDate),str(total_price)])
#     return render(request, 'sales_report.html', {'data':(data),'state_data':state_data,'district_data':[{'id':'1','name':'Thane'}]})


@login_required
@csrf_exempt
def get_recharge(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.Recharge.objects.all().values_list('user_id_farmer_id__first_name','user_id_farmer_id__last_name','user_id_farmer_id__username','updated_at','user_id_farmer_id__userprofile__state__state_name','user_id_farmer_id__userprofile__district__district_name','amount','id','status','user_id_retailer_id__first_name','user_id_retailer_id__last_name').order_by('-updated_at')
    for i in user_info:
        first_name=i[0]
        last_name=i[1]
        full_name=str(first_name)+" "+str(last_name)
        mobile_number=i[2]
        created_at=i[3]
        #formatedDate = created_at.strftime("%d-%m-%Y %H:%M:%S")
        formatedDate1= (created_at + timedelta(hours = 5,minutes = 30))
        formatedDate = formatedDate1.strftime("%d-%m-%Y %H:%M:%S")
        state=i[4]
        district=i[5]
        amount=i[6]
        id=i[7]
        status=i[8]
        full_name_retailer=str(i[9])+" "+str(i[10])

        if status:
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-content-id="+str(id)+">Recharge Done</button></div>"
        else:
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-content-id="+str(id)+">Recharge Now</button></div>"

        count+=1
        data.append([count,str(full_name),str(mobile_number),str(full_name_retailer),str(formatedDate),str(state),str(district),str(amount),btn])
    return render(request, 'manage_recharge.html', {'data':(data)})


@login_required
@csrf_exempt
def loyalty_retailer(request,pk):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserLoyaltyPoints.objects.filter(user_id_retailer_id=pk).values_list('user_id_retailer_id__first_name','user_id_retailer_id__last_name','user_id_retailer_id__username','user_id_retailer_id__userprofile__state__state_name','user_id_retailer_id__userprofile__district__district_name','loyalty_type','loyalty_point','order')
    for i in user_info:
        first_name=i[0]
        last_name=i[1]
        mobile_number=i[2]
        order_id=i[7]
        loyalty_type=i[5]
        loyalty_point=i[6]
        state=i[3]
        district=i[4]
        
        full_name=str(first_name)+" "+str(last_name)
        count+=1
        data.append([count,str(full_name),str(mobile_number),str(order_id),str(loyalty_type),str(loyalty_point),str(state),str(district)])
    return render(request, 'loyalty_retailer_view.html', {'data':(data)})


@csrf_exempt
def get_reports(request):
    from django.db.models import Q
    data=[]
    retailers_data=[]
    products_data=[]
    state=0
    district=0
    retailers_id=0
    count=0
    start_date=''
    searchDate=''
    end_date=''
    products_id=''
    state_data=get_state()
    retailers=models.UserProfile.objects.filter(user_type=2,user__is_active=1).values_list('user__id','user__first_name','user__last_name').order_by('-created_at')
    for i in retailers:
        retailers_data.append({'id':i[0],'full_name':i[1]+' '+i[2]})
        retailers_data=sorted(retailers_data, key=itemgetter('full_name'))

    products=models.Product.objects.filter(status=1).values_list('id','product_name').order_by('-created_at')
    for i in products:
        products_data.append({'id':i[0],'product_name':i[1]})
        products_data=sorted(products_data, key=itemgetter('product_name'))

    if request.GET.get('state'):
        state=request.GET.get('state')
    

    if request.GET.get('district'):
        district=request.GET.get('district')
    

    if request.GET.get('retailers'):
        retailers_id=request.GET.get('retailers')
    
    if request.GET.get('products'):
        products_id=request.GET.get('product')
    if request.GET.get('searchDate'):
        searchDate=request.GET.get('searchDate')
        daterange= searchDate.split(" - ")
        start_date=daterange[0]
        
        newDate=datetime.strptime(start_date, '%d/%m/%Y')
        start_date=newDate.strftime("%Y-%m-%d")
        
        end_date1=str(daterange[1])
        newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
        end_date=newDate.strftime("%Y-%m-%d")
        

    q = Q()
    if state:
        q &= Q(user_id_retailer_id__userprofile__state__id=state)
    if district:
        q &= Q(user_id_farmer_id__userprofile__district__id=district)
    if retailers_id:
        q &= Q(user_id_retailer_id=retailers_id)
    if products_id:
        q &= Q(product=products_id)
    if searchDate:
        q &= Q(created_at__range=(start_date, end_date))
    
    user_info1=models.Order.objects.filter(q).values_list('id','user_id_retailer_id__first_name','user_id_retailer_id__last_name','user_id_retailer_id__username','user_id_farmer_id__first_name','user_id_farmer_id__last_name','created_at','total_price','user_id_retailer_id__last_name','user_id_farmer_id__last_name','user_id_farmer_id__username').order_by('-updated_at')
    print("user_info1",user_info1.query)
    for i in user_info1:
        id=i[0]
        retailer_first_name=i[1]
        retailer_last_name=i[2]
        retailer_username=i[3]
        farmer__first_name=i[4]
        farmer_last_name=i[5]
        created_at=i[6]
        formatedDate = created_at.strftime("%d-%m-%Y")
        total_price=i[7]
        retailer_last_name=i[8]
        farmer_last_name=i[9]
        farmer_username=i[10]
        
        count+=1
        data.append([count,str(retailer_first_name)+' '+str(retailer_last_name),str(retailer_username),str(farmer__first_name)+' '+str(farmer_last_name),str(farmer_username),str(formatedDate),str(total_price)])
    return render(request, 'sales_report.html', {'data':(data),'state_data':state_data,'retailers':retailers_data,'products':products_data})



@csrf_exempt
def wholeseller_upload(request):
    template = "add_wholesaler.html"
    if request.method =='GET':
        return render(request, template)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not a CSV FILE")

    data_set = csv_file.read().decode('UTF-8')
    io_string =io.StringIO(data_set)
    next(io_string)
    count=0
    count1=0
    for i in csv.reader(io_string, delimiter = ',', quotechar="|"):
        username = i[0]
        password=username
        first_name=i[1]
        last_name=i[2]
        email=i[3]
        company_name=i[4]
        language=i[5]
        state=i[6]
        district=i[7]
        city=i[8]
        pincode=i[9]
        aadhar_no=i[10]
        address=i[11]
        gst_number=i[12]
        fertilizer_licence=i[13]
        fms_id=i[14]
        if User.objects.filter(username=username).exists():
            count+=1

        else:
            count1+=1
            new_user = User.objects.create(username = username,password = username,first_name=first_name,last_name=last_name,is_active=1,email=email)
            new_user.set_password(password)
            new_user.save()
            new_Uid = new_user.id

            user_type=Group.objects.get(id=4)
            user_type.user_set.add(new_Uid)
            langn_id=models.Language.objects.get(lang_name__icontains=language.strip().capitalize())
            state=models.State.objects.get(state_name__icontains=state.strip())
            district=models.District.objects.get(district_name__contains=district.strip().capitalize())
            if city:
                if models.City.objects.filter(city_name=city.strip().capitalize()).exists():
                    city_name=city
                else:
                    new_city = models.City.objects.create(city_name =city.strip().capitalize(),status=1)
                    new_city.save()
                    city_name=new_city.city_name
            # print('langn_id => '+str(langn_id))
            # print('first_name => '+str(first_name))
            # print('last_name => '+str(last_name))
            # print('email => '+str(email))
            # print('company_name => '+str(company_name))
            # print('state => '+str(state))
            # print('district => '+str(district))
            # print('city => '+str(city))
            # print('pincode => '+str(pincode))
            # print('address => '+str(address))
            # print('gst_number => '+str(gst_number))
            # print('fertilizer_licence => '+str(fertilizer_licence))
            # print('fms_id => '+str(fms_id))
            userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number)
            userprofile.save()

    # return render(request, 'add_wholesaler.html', {'data':(count),'state_data':count1})


    response=JsonResponse({'status':'success','Number_Of_User_Added':count1,'Number_Already_Exits':count})
    return response


def send_file(request):

    # import wget
    import os, tempfile, zipfile
    from wsgiref.util import FileWrapper
    from django.conf import settings
    import mimetypes
    import requests


    
    #template = "wholeseller_upload.html"
    filename     = "/opt/hurl/media/default/test.csv" # Select your file here.
    download_name ="sample_format.csv"
    # r = requests.get("home/dev04/workspace/hurl/media/default/test.csv")
    # response=urllib.request.urlretrieve(filename, '/Users/scott/Downloads/cat.jpg')

    wrapper      = FileWrapper(open(filename))
    response     = HttpResponse( wrapper,content_type='text/csv')
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
    


@csrf_exempt
def farmer_details_view(request,pk):
    data=[]
    retailers_data=[]
    products_data=[]
    products_id=''
    state_data=get_state()
    user_id=pk
    recharge_status=''
    count=0
    user_info1=models.Scratch.objects.filter(user_id_farmer_id=user_id).values_list('id','user_id_farmer_id__first_name','user_id_farmer_id__last_name','created_at','order__total_price','order__user_id_farmer_id__username','amount','order__id','user_id_farmer_id').order_by('-updated_at')
    for i in user_info1:
        id=i[0]
        farmer__first_name=i[1]
        farmer_last_name=i[2]
        created_at=i[3]
        formatedDate = created_at.strftime("%d-%m-%Y")
        total_price=i[4]
        farmer_username=i[5]
        amount=i[6]
        order_id=i[7]
        farmer_id=i[8]
        user_info12=models.Recharge.objects.filter(user_id_farmer_id=user_id).values_list('id','status')
        for i in user_info12:
            id1=i[0]
            status=i[1]
            if status:
                recharge_status="Complete"
                recharge_status="<lable class='btn btn-block btn-success btn-sm approve'>Complete</lable></div>"
            else:
                recharge_status="<lable class='btn btn-block btn-danger btn-sm disapprove'>Pending</lable></div>"

        count+=1
        data.append([count,str(farmer__first_name)+' '+str(farmer_last_name),str(farmer_username),str(order_id),str(total_price),str(amount),recharge_status,str(formatedDate),"<a class='btn' href='/order_details/"+str(order_id)+"'><i class='fas fa-eye'></i> View</a>"])

    return render(request, 'farmer_view.html', {'data':(data)})



@csrf_exempt
def recharge_report(request):
    data=[]
    farmer_phone_data=[]
    farmer_name_data=[]
    count=0
    searchDate=''
    user_id=''
    phone=''
    retailers=models.UserProfile.objects.filter(user_type=3,user__is_active=1).values_list('user__id','user__first_name','user__last_name','user__username').order_by('-created_at')
    for i in retailers:
        farmer_name_data.append({'id':i[0],'name':i[1]+' '+i[2]})
        farmer_phone_data.append({'id':i[0],'mobile_number':i[3]})
        farmer_phone_data=sorted(farmer_phone_data, key=itemgetter('mobile_number'))
        farmer_name_data=sorted(farmer_name_data, key=itemgetter('name'))

    if request.GET.get('user_id'):
        user_id=request.GET.get('user_id')
    
    if request.GET.get('phone'):
        phone=request.GET.get('phone')
    if request.GET.get('searchDate'):
        searchDate=request.GET.get('searchDate')
        daterange= searchDate.split(" - ")
        start_date=daterange[0]
        
        newDate=datetime.strptime(start_date, '%d/%m/%Y')
        start_date=newDate.strftime("%Y-%m-%d")
        
        end_date1=str(daterange[1])
        newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
        end_date=newDate.strftime("%Y-%m-%d")

    q = Q()
    if user_id:
        q |= Q(user_id_farmer_id__id=user_id)
    if phone:
        q |= Q(user_id_farmer_id__username=phone)
    if searchDate:
        q &= Q(order__created_at__range=(start_date, end_date))
    user_info1=models.Recharge.objects.filter(q).values_list('id','user_id_farmer_id__first_name','user_id_farmer_id__last_name','order__created_at','user_id_farmer_id__username','amount').order_by('-updated_at')
    print("user_info1",user_info1.query)
    for i in user_info1:
        id=i[0]
        farmer__first_name=i[1]
        farmer_last_name=i[2]
        created_at=i[3]
        formatedDate = created_at.strftime("%d-%m-%Y")
        mobile_number=i[4]
        amount=i[5]

        count+=1
        data.append([count,str(formatedDate),str(farmer__first_name)+' '+str(farmer_last_name),str(mobile_number),str(amount)])

    return render(request, 'recharge_report.html', {'data':(data),'farmer_name_data':farmer_name_data,'farmer_phone_data':farmer_phone_data})


@csrf_exempt
def loyalty_point_report(request):
    data=[]
    retailer_phone_data=[]
    retailer_name_data=[]
    count=0
    searchDate=''
    user_id=''
    phone=''
    retailers=models.UserProfile.objects.filter(user_type=2,user__is_active=1).values_list('user__id','user__first_name','user__last_name','user__username').order_by('-created_at')
    for i in retailers:
        retailer_name_data.append({'id':i[0],'name':i[1]+' '+i[2]})
        retailer_phone_data.append({'id':i[0],'mobile_number':i[3]})
        retailer_phone_data=sorted(retailer_phone_data, key=itemgetter('mobile_number'))
        retailer_name_data=sorted(retailer_name_data, key=itemgetter('name'))

    if request.GET.get('user_id'):
        user_id=request.GET.get('user_id')
    
    if request.GET.get('phone'):
        phone=request.GET.get('phone')
    if request.GET.get('searchDate'):
        searchDate=request.GET.get('searchDate')
        daterange= searchDate.split(" - ")
        start_date=daterange[0]
        
        newDate=datetime.strptime(start_date, '%d/%m/%Y')
        start_date=newDate.strftime("%Y-%m-%d")
        
        end_date1=str(daterange[1])
        newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
        end_date=newDate.strftime("%Y-%m-%d")

    q = Q()
    if user_id:
        q |= Q(user_id_retailer_id__id=user_id)
    if phone:
        q |= Q(user_id_retailer_id__username=phone)
    if searchDate:
        q &= Q(created_at__range=(start_date, end_date))
    user_info1=models.UserLoyaltyPoints.objects.filter(q).values_list('id','user_id_retailer_id__first_name','user_id_retailer_id__last_name','created_at','user_id_retailer_id__username','loyalty_point','loyalty_type').order_by('-updated_at')
    print("user_info1",user_info1.query)
    for i in user_info1:
        id=i[0]
        farmer__first_name=i[1]
        farmer_last_name=i[2]
        created_at=i[3]
        formatedDate = created_at.strftime("%d-%m-%Y")
        mobile_number=i[4]
        amount=i[5]
        Loyalty_type=i[6]

        count+=1
        data.append([count,str(formatedDate),str(farmer__first_name)+' '+str(farmer_last_name),str(mobile_number),str(amount),str(Loyalty_type)])

    return render(request, 'loyalty_point_report.html', {'data':(data),'retailer_name_data':retailer_name_data,'retailer_phone_data':retailer_phone_data})



@csrf_exempt
def get_notifications(request):
    data=[]
    count=0

    user_info=models.Notification.objects.all().values_list('title_eng','created_at','status','district_id','state_id','group_id','push_status','sms_status','id').order_by('-created_at')
    
    for i in user_info:
        title_eng=i[0]
        created_at=i[1]
        formatedDate = created_at.strftime("%d-%m-%Y")
        district=i[3]
        if district != 0:
            district=models.District.objects.get(id=district)
        else:
            district="-"
        state=i[4]
        if state != 0:
            state=models.State.objects.get(id=state)
        else:
            state="-"
        status=i[2]
        group=i[5]
        grouTxt=''
        if(group):
            Arr=group.split(',')
            for gid in Arr:
                grouTxt=str(Group.objects.get(id=gid))+','+str(grouTxt)
        push_request=i[6]
        push='No'
        if push_request == 1:
            push='Yes'
        sms_request=i[7]   
        sms='No'
        if sms_request == 1:
            sms='Yes'
        id=i[8]
        
        count+=1
        data.append([count,str(title_eng),str(district),str(state),str(grouTxt[:-1]),formatedDate,push,sms])
    return render(request, 'manage_notifications.html', {'data':(data)})

@csrf_exempt
def add_notifications(request):
	import requests
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

	lang_data=get_langauge()
	state_data=get_state()
	if request.method == 'POST':
	    data={}
	    sms_response=''
	    push_response=''
	    push_service = FCMNotification(api_key="AAAAT-fnF2g:APA91bEWQbMJqFFPIy-zTLllngov5w09ed6u5MS3pUKLOq9GrVmq7HPxQCDWirrq4wGjYUI2v1vQP-IHQARgO3atV1LU_QM7vtWpEYo0ashQ7NiBdxCR8DneRWZ-OQwCaoxpWTXS7mA-")
	    user_type_get=request.POST.getlist('user_type[]')
	    group_id = ','.join(user_type_get)
	    title_eng = request.POST.get('title_eng')
	    title_hnd = request.POST.get('title_hnd')
	    request_for = request.POST.getlist('request_for[]')
	    sms_status='0'
	    push_status='0'
	    if 'push' in request_for:
	        push_status='1'
	    
	    if 'sms' in request_for:
	        sms_status='1'
	    
	    message_eng = request.POST.get('message_eng')
	    message_hnd = request.POST.get('message_hnd')
	    status = '1'
	    district_id = request.POST.get('district')
	    if district_id == '':
	       district_id=0
	    else:
	       district_id=district_id  
	    state_id = request.POST.get('state')
	    if state_id == '':
	       state_id=0
	    else:
	       state_id=state_id

	    q = Q()
	    if '2' in user_type_get:
	        q |= Q(user_type=2)
	    if '3' in user_type_get:
	        q |= Q(user_type=3)
	    if '4' in user_type_get:
	        q |= Q(user_type=4)
	    user_info=models.UserProfile.objects.filter(q).values_list('user__username','language_id','fcm_id').order_by('-created_at')
	    #print(user_info.query)
	    for i in user_info:
	        mobile=i[0]
	        language_code=i[1]
	        if language_code == '1':
	            title=title_eng
	            message=message_eng
	        else:
	            title=title_hnd
	            message=message_hnd
	        fcm_id=i[2]
	        if push_status == '1':
	            print('Push Notification code')
                if fcm_id:
                    registration_id = fcm_id
                    message_title = title
                    message_body = message
                    
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body,message_icon='notification_icon')
                    print(result)
                    push_response=str(result)+'<br>'+push_response
	        if sms_status =='1':
	            print('SMS code')
	            Phone_number = mobile
	            sms_url="http://sms.peakpoint.co/sendsmsv2.asp"

	            data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":str(message)}
	            requests.packages.urllib3.disable_warnings()
	            r = requests.post(sms_url,data = data)
	            sms_response=r.content+'<br>'+sms_response
	    Content = models.Notification.objects.create(title_eng=title_eng,title_hnd=title_hnd,message_eng=message_eng,message_hnd=message_hnd,push_status=push_status,sms_status=sms_status,push_response=push_response,sms_response=sms_response,status=status,district_id=district_id,group_id=group_id,state_id=state_id,created_at=datetime.now())
	    Content.save()
	    response=JsonResponse({'status':'success'})
	    return response
	else:
	    data={'languages':lang_data,'state_data':state_data}
	    return render(request, 'add-notification.html', {'data':data})


@csrf_exempt
def loyalty_configuration(request):
    userdata=models.LoyaltyPoints.objects.all().values_list('id','loyalty_type','loyalty_point')
    data=[]
    count=1
    for nlist in userdata:
        loyalty_id=nlist[0]
        loyalty_type=nlist[1]
        loyalty_point=nlist[2]
        data.append([count,str(loyalty_type),loyalty_point,"<a href='/edit_loyalty/"+str(loyalty_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
        count+=1
    return render(request, 'loyalty_configuration.html', {'data':data})

@csrf_exempt
def loyalty_configuration_farmer(request):
    userdata=models.LoyaltyPoints.objects.filter(loyalty_type='Order').values_list('id','loyalty_type','loyalty_point')
    data=[]
    count=1
    for nlist in userdata:
        loyalty_id=nlist[0]
        loyalty_type=nlist[1]
        loyalty_point=nlist[2]
        data.append([count,str(loyalty_type),loyalty_point,"<a href='/edit_loyalty/"+str(loyalty_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
        count+=1
    return render(request, 'loyalty_configuration_farmer.html', {'data':data})

@csrf_exempt
def edit_loyalty(request,pk):
    loyalty_id=pk
    if request.method == 'POST':
        loyalty_type=request.POST.get('loyalty_type')
        loyalty_point=request.POST.get('loyalty_point')
        loyalty= models.LoyaltyPoints.objects.get(id=loyalty_id)
        loyalty.loyalty_type=loyalty_type
        loyalty.loyalty_point=int(loyalty_point)
        loyalty.conversion=0
        loyalty.updated_at=datetime.now()
        loyalty.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        userdata=models.LoyaltyPoints.objects.filter(id=loyalty_id).values_list('id','loyalty_type','loyalty_point')
        data=[]
        count=1
        for nlist in userdata:
            loyalty_id=nlist[0]
            loyalty_type=nlist[1]
            loyalty_point=nlist[2]
        count+=1
        data={"loyalty_id":loyalty_id,"loyalty_type":loyalty_type,"loyalty_point":loyalty_point}
        count+=1
        return render(request, 'edit_loyalty.html', {'data':data})


@csrf_exempt
def loyalty_configuration(request):
    userdata=models.LoyaltyPoints.objects.all().values_list('id','loyalty_type','loyalty_point')
    data=[]
    count=1
    for nlist in userdata:
        loyalty_id=nlist[0]
        loyalty_type=nlist[1]
        loyalty_point=nlist[2]
        data.append([count,str(loyalty_type),loyalty_point,"<a href='/edit_loyalty/"+str(loyalty_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
        count+=1
    return render(request, 'loyalty_configuration.html', {'data':data})

# @csrf_exempt
# def loyalty_configuration_farmer(request):
#     productdata=models.FarmerRechargeConfiguration.objects.all().values_list('id','product__product_name','product__product_unit_name','quantity','recharge_amount')
#     data=[]
#     count=1
#     for nlist in productdata:
#         conf_id=nlist[0]
#         product_name=nlist[1]
#         product_unit_name=nlist[2]
#         quantity=nlist[3]
#         recharge_amount=nlist[4]
#         data.append([count,str(product_name),str(product_unit_name),str(quantity),str(recharge_amount),"<a href='/edit_user/"+str(conf_id)+"' class='btn'><i class='fas fa-edit'></i>Edit</a>"])
#     count+=1
#     return render(request, 'loyalty_configuration_farmer.html', {'data':data})

@csrf_exempt
def loyalty_configuration_farmer(request):
    productdata=models.FarmerRechargeConfiguration.objects.all().values_list('id','product__product_name','product__product_unit_name','quantity','recharge_amount').order_by('-created_at')
    data=[]
    count=0
    for nlist in productdata:
        count+=1
        conf_id=nlist[0]
        product_name=nlist[1]
        product_unit_name=nlist[2]
        quantity=nlist[3]
        recharge_amount=nlist[4]
        data.append([count,str(product_name),str(product_unit_name),str(quantity),str(recharge_amount),"<a href='/edit_loyalty_configuration/"+str(conf_id)+"' class='btn'><i class='fas fa-edit'></i>Edit</a>"])
    return render(request, 'loyalty_configuration_farmer.html', {'data':data})

@csrf_exempt
def edit_loyalty_configuration(request,pk):
    products_data=[]
    if request.method == 'POST':
        product_id=request.POST.get('product_name')
        quantity=request.POST.get('quantity')
        recharge_amount=request.POST.get('recharge_amount')
        print("product_idproduct_id",product_id)
        conf_data = models.FarmerRechargeConfiguration.objects.get(id=pk)
        product_id=models.Product.objects.get(id=product_id)
        conf_data.product = product_id
        conf_data.quantity = quantity
        conf_data.recharge_amount = recharge_amount
        conf_data.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        productdata=models.FarmerRechargeConfiguration.objects.all().values_list('id','product__product_name','product__product_unit','quantity','recharge_amount','product_id')
        data=[]
        count=1
        for nlist in productdata:
            conf_id=nlist[0]
            product_name=nlist[1]
            product_unit=nlist[2]
            quantity=nlist[3]
            recharge_amount=nlist[4]
            product_id=nlist[5]
            data={"conf_id":conf_id,"product_name":product_name,"product_unit_name":product_unit,"quantity":quantity,"recharge_amount":recharge_amount,"product_id":product_id}
        products=models.Product.objects.filter(status=1).values_list('id','product_name').order_by('-created_at')
        for i in products:
            products_data.append({'id':i[0],'product_name':i[1]})
            products_data=sorted(products_data, key=itemgetter('product_name'))
        return render(request, 'edit_loyality_configuration.html',  {'data':(data),'products_data':products_data})


@csrf_exempt
def add_famer_configuration(request):
    products_data=[]
    if request.method == 'POST':
        product_id=request.POST.get('product_name')
        product_id=models.Product.objects.get(id=product_id)
        quantity=request.POST.get('quantity')
        recharge_amount=request.POST.get('recharge_amount')
        farmer_conf = models.FarmerRechargeConfiguration.objects.create(product = product_id,quantity = quantity,recharge_amount=recharge_amount)
        farmer_conf.save()
        response=JsonResponse({'status':'success'})
        return response
    else:
        productdata=models.FarmerRechargeConfiguration.objects.all().values_list('id','product__product_name','product__product_unit','quantity','recharge_amount')
        data=[]
        count=1
        for nlist in productdata:
            conf_id=nlist[0]
            product_name=nlist[1]
            product_unit=nlist[2]
            quantity=nlist[3]
            recharge_amount=nlist[4]
            data.append([count,str(product_name+" "+product_unit),str(quantity),str(recharge_amount)])
        count+=1
        products=models.Product.objects.filter(status=1).values_list('id','product_name').order_by('-created_at')
        for i in products:
            products_data.append({'id':i[0],'product_name':i[1]})
            products_data=sorted(products_data, key=itemgetter('product_name'))

        print("data",data,products_data)
        return render(request, 'add_famer_configuration.html',  {'data':(data),'products_data':products_data})



@csrf_exempt
def edit_loyalty(request):
    data=[]
    if request.method == 'POST':
        type_list=request.POST.getlist('loyalty_point[]')
        order_type=type_list[0]
        reg_type=type_list[1]
        if order_type:
            loyalty= models.LoyaltyPoints.objects.get(loyalty_type='Order')
            loyalty.loyalty_point=int(order_type)
            loyalty.conversion=0
            loyalty.updated_at=datetime.now()
            loyalty.save()
        if reg_type:
            loyalty= models.LoyaltyPoints.objects.get(loyalty_type='Registration')
            loyalty.loyalty_point=int(reg_type)
            loyalty.conversion=0
            loyalty.updated_at=datetime.now()
            loyalty.save()

        response=JsonResponse({'status':'success'})
        return response
    else:
        userdata=models.LoyaltyPoints.objects.all().values_list('id','loyalty_type','loyalty_point')
        data=[]
        count=1
        for nlist in userdata:
            loyalty_id=nlist[0]
            loyalty_type=nlist[1]
            loyalty_point=nlist[2]
            data.append({"loyalty_id":loyalty_id,"loyalty_type":loyalty_type,"loyalty_point":loyalty_point})
        count+=1
    print("data",data)
    return render(request, 'edit_loyalty.html', {'data':data})

@csrf_exempt
def recharge_report(request):
    data=[]
    farmer_phone_data=[]
    farmer_name_data=[]
    count=0
    searchDate=''
    user_id=''
    phone=''
    retailers=models.UserProfile.objects.filter(user_type=3,user__is_active=1).values_list('user__id','user__first_name','user__last_name','user__username').order_by('-created_at')
    for i in retailers:
        farmer_name_data.append({'id':i[0],'name':i[1]+' '+i[2]})
        farmer_phone_data.append({'id':i[0],'mobile_number':i[3]})
        farmer_phone_data=sorted(farmer_phone_data, key=itemgetter('mobile_number'))
        farmer_name_data=sorted(farmer_name_data, key=itemgetter('name'))

    if request.GET.get('user_id'):
        user_id=request.GET.get('user_id')
    
    if request.GET.get('phone'):
        phone=request.GET.get('phone')
    if request.GET.get('searchDate'):
        searchDate=request.GET.get('searchDate')
        daterange= searchDate.split(" - ")
        start_date=daterange[0]
        
        newDate=datetime.strptime(start_date, '%d/%m/%Y')
        start_date=newDate.strftime("%Y-%m-%d")
        
        end_date1=str(daterange[1])
        newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
        end_date=newDate.strftime("%Y-%m-%d")

    q = Q()
    if user_id:
        q |= Q(user_id_farmer_id__id=user_id)
    if phone:
        q |= Q(user_id_farmer_id__username=phone)
    if searchDate:
        q &= Q(order__created_at__range=(start_date, end_date))
    user_info1=models.Recharge.objects.filter(q).values_list('id','user_id_farmer_id__first_name','user_id_farmer_id__last_name','order__created_at','user_id_farmer_id__username','amount').order_by('-updated_at')
    print("user_info1",user_info1.query)
    for i in user_info1:
        id=i[0]
        farmer__first_name=i[1]
        farmer_last_name=i[2]
        created_at=i[3]
        formatedDate = created_at.strftime("%d-%m-%Y")
        mobile_number=i[4]
        amount=i[5]

        count+=1
        data.append([count,str(formatedDate),str(farmer__first_name)+' '+str(farmer_last_name),str(mobile_number),str(amount)])

    return render(request, 'recharge_report.html', {'data':(data),'farmer_name_data':farmer_name_data,'farmer_phone_data':farmer_phone_data})


# @csrf_exempt
# def loyalty_point_report(request):
#     data=[]
#     retailer_phone_data=[]
#     retailer_name_data=[]
#     count=0
#     searchDate=''
#     user_id=''
#     phone=''
#     retailers=models.UserProfile.objects.filter(user_type=2,user__is_active=1).values_list('user__id','user__first_name','user__last_name','user__username').order_by('-created_at')
#     for i in retailers:
#         retailer_name_data.append({'id':i[0],'name':i[1]+' '+i[2]})
#         retailer_phone_data.append({'id':i[0],'mobile_number':i[3]})
#         retailer_phone_data=sorted(retailer_phone_data, key=itemgetter('mobile_number'))
#         retailer_name_data=sorted(retailer_name_data, key=itemgetter('name'))

#     if request.GET.get('user_id'):
#         user_id=request.GET.get('user_id')
    
#     if request.GET.get('phone'):
#         phone=request.GET.get('phone')
#     if request.GET.get('searchDate'):
#         searchDate=request.GET.get('searchDate')
#         daterange= searchDate.split(" - ")
#         start_date=daterange[0]
        
#         newDate=datetime.strptime(start_date, '%d/%m/%Y')
#         start_date=newDate.strftime("%Y-%m-%d")
        
#         end_date1=str(daterange[1])
#         newDate=datetime.strptime(end_date1, '%d/%m/%Y') + timedelta(days=1)
#         end_date=newDate.strftime("%Y-%m-%d")

#     q = Q()
#     if user_id:
#         q |= Q(user_id_retailer_id__id=user_id)
#     if phone:
#         q |= Q(user_id_retailer_id__username=phone)
#     if searchDate:
#         q &= Q(created_at__range=(start_date, end_date))
#     user_info1=models.UserLoyaltyPoints.objects.filter(q).values_list('id','user_id_retailer_id__first_name','user_id_retailer_id__last_name','created_at','user_id_retailer_id__username','loyalty_point').order_by('-updated_at')
#     print("user_info1",user_info1.query)
#     for i in user_info1:
#         id=i[0]
#         farmer__first_name=i[1]
#         farmer_last_name=i[2]
#         created_at=i[3]
#         formatedDate = created_at.strftime("%d-%m-%Y")
#         mobile_number=i[4]
#         amount=i[5]

#         count+=1
#         data.append([count,str(formatedDate),str(farmer__first_name)+' '+str(farmer_last_name),str(mobile_number),str(amount)])

#     return render(request, 'loyalty_point_report.html', {'data':(data),'retailer_name_data':retailer_name_data,'retailer_phone_data':retailer_phone_data})

@csrf_exempt
def get_product_unit(request,pk):
    product_info=models.Product.objects.filter(id=pk).values_list('product_unit_name')
    response=JsonResponse({'status':'success','unit':product_info[0][0]})
    return response

@csrf_exempt
def user_status_active_deactive(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Activate Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Deactivate Successfuly'})
        return response

@csrf_exempt
def user_status_farmer(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Farmer Activate Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Farmer Deactivate Successfuly'})
        return response


@csrf_exempt
def sendapprove(full_name,status,mobile_number) :
   import requests
   #digits = "0123456789"
   OTP = ""
   # Phone_number=mobile_number
   Phone_number = mobile_number
   full_name=full_name
   sms_url="http://sms.peakpoint.co/sendsmsv2.asp"
   data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":"Hello "+full_name+",\nYour Apna urea profile has been "+status+", you can login to the App using the phone number "+Phone_number+"\nTeam Hurl"}
   requests.packages.urllib3.disable_warnings()
   r = requests.post(sms_url,data = data)
   return OTP


@csrf_exempt
def user_status_retailer(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Retailer Activate Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Retailer Deactivate Successfuly'})
        return response


@csrf_exempt
def user_status_wholesaler(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Wholesaler Activate Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'Wholesaler Deactivate Successfuly'})
        return response

