# dappx/views.py
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
from hurlapp.models import UserProfile,Product
from hurlapp import forms
from hurl import settings
import os
# import xlsxwriter 

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
def dashboard(request):
    total_farmer=UserProfile.objects.filter(user_type_id='3').count()
    total_wholeseler=UserProfile.objects.filter(user_type_id='4').count()
    total_retailer=UserProfile.objects.filter(user_type_id='2').count()
    total_product=Product.objects.filter(status='1').count()
    data={'total_farmer':total_farmer,'total_wholeseler':total_wholeseler,"total_retailer":total_retailer,"total_product":total_product}
    return render(request,'dashboard.html',{'data':data})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data={}
        username = request.POST.get('mobile_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        data={'username':username,'password':password,"status":True}
        
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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'userprofile.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})
       

# def add_state(request):
#     add = models.State.object.create(JAMMU & KASHMIR,HIMACHAL PRADESH,PUNJAB,CHANDIGARH,UTTARANCHAL,HARYANA,DELHI,RAJASTHAN,UTTAR PRADESH,BIHAR,SIKKIM,ARUNACHAL PRADESH,NAGALAND,MIZORAM,TRIPURA,MEGHALAYA,ASSAM,WEST BENGAL,JHARKHAND,CHHATTISGARH,MADHYA PRADESH,GUJARAT,DAMAN & DIU,DADRA & NAGAR HAVELI,MAHARASHTRA,ANDHRA PRADESH,KARNATAKA,LAKSHADWEEP,KERALA,TAMIL NADU,ANDAMAN & NICOBAR ISLANDS,)
#     response = JsonResponse({'status':'success'})
#         return response


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

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email)

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

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email)

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
            print("user_photo",user_photo)
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
        response=JsonResponse({'status':'success','msg':'User Approved Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
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

@csrf_exempt
def user_status(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Approved Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Disapproved Successfuly'})
        return response

def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],}
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
        case2 = {'id': i[0], 'name': i[1]}
        state_data.append(case2)
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
    product_info=models.Product.objects.all().values_list('product_image','product_name','product_code','product_unit','product_unit_name','product_price','status','id')
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
            btn="<div class='editBut'><button class='btn btn-block btn-danger btn-sm disapprove' data-product-id="+str(product_id)+">Disapprove</button></div>"
        else:
            status="Deactive"
            btn="<div class='editBut'><button class='btn btn-block btn-success btn-sm approve' data-product-id="+str(product_id)+">Approve</button></div>"
        count+=1
        data.append([count,'<img src="'+str(product_image)+'"  width="70" height="50">',str(product_name),str(product_code),str(product_unit),str(product_price),status,btn,"<a href='/edit_product/"+str(product_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a>"])
#     return render(request, 'get_product.html', {'data':(data)})
    return render(request, 'get_product.html', {'data':(data)})

@csrf_exempt
def edit_product(request,pk):
    print("Add USer")
    product_id=pk
    if request.method == 'POST':
        data={}
        product_image=''
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        product_unit = request.POST.get('product_unit')
        product_unit_name = request.POST.get('product_unit_name')
        product_price = request.POST.get('product_price')
        if request.FILES.get('product_image'):
            product_image = request.FILES['product_image']

        product = Product.objects.get(id=pk)
        product.product_name=product_name
        product.product_code=product_code
        product.product_unit=product_unit
        product.product_unit_name=product_unit_name
        product.product_price=product_price
        product.product_image=product_image
        product.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        product_info=models.Product.objects.filter(id=pk).values_list('product_image','product_name','product_code','product_unit','product_price','status','id')
        print(product_info)
        data={'product_image':'/'+product_info[0][0],'product_name':product_info[0][1],'product_code':product_info[0][2],'product_unit':product_info[0][3],'product_price':product_info[0][4],'product_id':product_info[0][6]}
        print(data)
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
        
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email)

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
            print("user_photo",user_photo)
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
            print("user_photo1",user_photo1)
            # if user_photo1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(user_photo1[0]))
            user_photo = request.FILES['user_photo']
            user_profile.user_photo = user_photo
            
        if request.FILES.get('aadhar_card'):
            # if aadhar_card1:
            #     os.remove(settings.BASE_DIR+settings.MEDIA_URL+str(aadhar_card1[0]))
            aadhar_card = request.FILES['aadhar_card']
            print("sssssss",aadhar_card)
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

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,email=email)

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
            print("user_photo",user_photo)
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

@csrf_exempt
def user_status(request):
    status=request.POST.get('status')
    user_id=request.POST.get('user_id')
    if status=="Deactive":
        user_details=User.objects.get(id=user_id)
        user_details.is_active=1
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Approved Successfuly'})
        return response
    else:
        user_details=User.objects.get(id=user_id)
        user_details.is_active=0
        user_details.save()
        response=JsonResponse({'status':'success','msg':'User Disapproved Successfuly'})
        return response

def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],}
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
        case2 = {'id': i[0], 'name': i[1]}
        state_data.append(case2)
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
    print("Call")
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




@csrf_exempt
def add_product(request):
    print("Add USer")
    if request.method == 'POST':
        data={}
        product_image=''
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        product_unit = request.POST.get('product_unit')
        product_unit_name = request.POST.get('product_unit_name')
        print("product_unit_name",product_unit_name)
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
        print("Post Data Retailer")
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
        else:
            status="Deactive"


        count+=1
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),"<a href='/edit_retailer/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-gift'></i> Layalty Points</a>"])
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
        user_type = 2
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
        else:
            status="Deactive"


        count+=1
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),"<a href='/edit_farmer/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
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
        print("Post Data Farmer")
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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area,fertilizer_photo=fertilizer_photo,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number)
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
        else:
            status="Deactive"


        count+=1
        if full_name=="Hurl Admin":
            pass
        else:
            data.append([count,str(full_name),str(username),str(district),str(state), str(status),"<a href='/edit_wholesaler/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/user_profile/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_wholesaler.html', {'data':(data)})

@csrf_exempt
def import_wholesaler(request):
    import pandas as pd
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR = os.path.join(BASE_DIR,'media')
    print("hieeeeeeeeee",MEDIA_DIR)
    data = pd.read_excel (MEDIA_DIR+'/1.xlsx') 
    df = pd.DataFrame(data, columns= ['name'])
    print (df)
    input()
    # new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
    # new_user.set_password(password)
    # new_user.save()
    # new_Uid = new_user.id
    # user_type=Group.objects.get(id=user_type)
    # user_type.user_set.add(new_Uid)
    # langn_id=models.Language.objects.get(id=langn_id)
    # state=models.State.objects.get(id=state)
    # district=models.District.objects.get(id=district)
    # if city:
    #     if models.City.objects.filter(city_name=city).exists():
    #         city_name=city
    #     else:
    #         new_city = models.City.objects.create(city_name =city,status=1)
    #         new_city.save()
    #         city_name=new_city.city_name
    # userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
    # userprofile.save()
    # response=JsonResponse({'status':'success'})
    # return response

@login_required
@csrf_exempt
def get_order(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=3).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
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
        else:
            status="Deactive"


        count+=1
        data.append([count,str(full_name),str(username),str(district),str(state), str(status),"","","",user_id])
    return render(request, 'manage_farmer.html', {'data':(data)})

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
        user = models.Product.objects.create(product_name=product_name,product_unit=product_unit)
        user.save()
        #remember_me = request.POST.get('remember_me')
        #print("Insideeee",remember_me)
        data={'product_name':product_name,'product_unit':product_unit,"status":True}
        return render(request, 'order.html', {})

    else:
        #return render(request, 'login.html', {})
        return render(request, 'order.html', {})

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
def download_sample(request):
    # import xlsxwriter module 
    import xlsxwriter 
    workbook = xlsxwriter.Workbook('add_wholesaler.xlsx')

      
    # By default worksheet names in the spreadsheet will be  
    # Sheet1, Sheet2 etc., but we can also specify a name. 
    worksheet = workbook.add_worksheet("My sheet") 
      
    worksheet1 = workbook.add_worksheet()        # Defaults to Sheet1.
    worksheet3 = workbook.add_worksheet() 
      
    # Start from the first cell. Rows and 
    # columns are zero indexed. 
    expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
    )

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()

from wsgiref.util import FileWrapper
@csrf_exempt
def download_pdf(request):
    filename = 'add_wholesaler.xlsx'
    content = FileWrapper(filename)
    response = HttpResponse(content, content_type='application/xlsx')
    return response
