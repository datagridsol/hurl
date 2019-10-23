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
from hurlapp.models import UserProfile
from hurlapp import forms
from hurl import settings
import os

def index(request):
    return render(request,'index.html')

def permission(request):
     return HttpResponse("You dont have permission")
@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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
def dashboard(request):
    return render(request,'dashboard.html')
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
        print("Post Data")
        data={}
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        username = request.POST.get('username')
        password = request.POST.get('username')
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

        if request.FILES.get('user_photo'):
            user_photo = request.FILES['user_photo']
            #folerval=image_upload_location(username,user_photo,'user')
            
        if request.FILES.get('aadhar_card'):
            aadhar_card = request.FILES['aadhar_card']
        if request.FILES.get('pan_card'):
            pan_card = request.FILES['pan_card']
        if request.FILES.get('vote_id'):
            vote_id = request.FILES['vote_id']
        if request.FILES.get('soil_card'):
            soil_card = request.FILES['soil_card']
        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        user_photo=request.POST.get('user_photo')
        aadhar_card=request.POST.get('aadhar_card')
        pan_card=request.POST.get('pan_card')
        vote_id=request.POST.get('vote_id')
        land_area=request.POST.get('land_area')
    
        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=0,email=email)
        land_area=request.POST.get('land_area')

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=1,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        #print("5444444444444",models.get_image_filename(get_image_filename))
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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'userprofile.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})
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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response



@csrf_exempt
def edit_user(request, pk):
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
    user_id=pk
    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

    if request.method == 'POST':
        data={}
        user_id = request.POST.get('user_id')
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
        user_photo=request.POST.get('user_photo')
        aadhar_card=request.POST.get('aadhar_card')
        pan_card=request.POST.get('pan_card')
        vote_id=request.POST.get('vote_id')
        soil_card=request.POST.get('soil_card')
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,is_active=0,email=email)
        
        user_type=Group.objects.get(id=user_type)
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
        models.UserProfile.objects.filter(user_id=user_id).update(user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
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
            user_photo=i[12]
            aadhar_card=i[13]
            pan_card=i[14]
            vote_id=i[15]
            soil_card=i[16]
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}],"user_id":user_id}
            
        return render(request, 'edit_user.html',{'data':data})

@csrf_exempt
def edit_retailer(request, pk):
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

    if request.method == 'POST':
        data={}
        user_id =pk
        #password = request.POST.get('mobile_number')
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
        #user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        print("aadhar_noaadhar_no",state)
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        user_photo=request.POST.get('user_photo')
        aadhar_card=request.POST.get('aadhar_card')
        pan_card=request.POST.get('pan_card')
        vote_id=request.POST.get('vote_id')
        soil_card=request.POST.get('soil_card')
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,is_active=0,email=email)
        
        #user_type=Group.objects.get(id=user_type)
        print("langn_idlangn_id",langn_id)
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
        print("aadhar_no11111111",user_id)
        models.UserProfile.objects.filter(user_id=user_id).update(parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
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
            user_photo=i[12]
            aadhar_card=i[13]
            pan_card=i[14]
            vote_id=i[15]
            soil_card=i[16]
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":"media/media/Screenshot_from_2019-10-18_16-21-35.png","pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]}
            # data.append([str(user_type),str(language),str(full_name),str(email),str(mobile_number),str(state),str(city),str(district),str(pincode),str(address),str(user_photo),str(pan_card),str(vote_id),str(soil_card),str(land_area)])
        return render(request, 'edit_retailer.html',{'data':data})


@csrf_exempt
def edit_farmer(request, pk):
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

    if request.method == 'POST':
        data={}
        user_id =pk
        #password = request.POST.get('mobile_number')
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
        #user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        print("aadhar_noaadhar_no",state)
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        user_photo=request.POST.get('user_photo')
        aadhar_card=request.POST.get('aadhar_card')
        pan_card=request.POST.get('pan_card')
        vote_id=request.POST.get('vote_id')
        soil_card=request.POST.get('soil_card')
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,is_active=0,email=email)
        
        #user_type=Group.objects.get(id=user_type)
        print("langn_idlangn_id",langn_id)
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
        print("aadhar_no11111111",user_id)
        models.UserProfile.objects.filter(user_id=user_id).update(parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
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
            user_photo=i[12]
            aadhar_card=i[13]
            pan_card=i[14]
            vote_id=i[15]
            soil_card=i[16]
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":"media/media/Screenshot_from_2019-10-18_16-21-35.png","pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]}
            # data.append([str(user_type),str(language),str(full_name),str(email),str(mobile_number),str(state),str(city),str(district),str(pincode),str(address),str(user_photo),str(pan_card),str(vote_id),str(soil_card),str(land_area)])
        return render(request, 'edit_farmer.html',{'data':data})


@csrf_exempt
def edit_wholesaler(request, pk):
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

    if request.method == 'POST':
        data={}
        user_id =pk
        #password = request.POST.get('mobile_number')
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
        #user_type = request.POST.get('user_type')
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        print("aadhar_noaadhar_no",state)
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        user_photo=request.POST.get('user_photo')
        aadhar_card=request.POST.get('aadhar_card')
        pan_card=request.POST.get('pan_card')
        vote_id=request.POST.get('vote_id')
        soil_card=request.POST.get('soil_card')
        land_area=request.POST.get('land_area')

        models.User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,is_active=0,email=email)
        
        #user_type=Group.objects.get(id=user_type)
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
        models.UserProfile.objects.filter(user_id=user_id).update(parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
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
            user_photo=i[12]
            aadhar_card=i[13]
            pan_card=i[14]
            vote_id=i[15]
            soil_card=i[16]
            land_area=i[17]
            group_id=i[18]
            lang_id=i[19]
            state_id=i[20]
            district_id=i[21]
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":"media/media/Screenshot_from_2019-10-18_16-21-35.png","pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]}
            # data.append([str(user_type),str(language),str(full_name),str(email),str(mobile_number),str(state),str(city),str(district),str(pincode),str(address),str(user_photo),str(pan_card),str(vote_id),str(soil_card),str(land_area)])
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

# @csrf_exempt
# def get_manage_user(request):
#     data=[]
#     user_type=""
#     district=""
#     state=""
#     count=0
#     userdata=User.objects.filter(~Q(id=1)).values_list('id', 'first_name','last_name','username','is_active')
#     for nlist in userdata:
#         row=[]
#         user_id=nlist[0]
#         first_name=nlist[1]
#         last_name=nlist[2]
#         full_name=str(first_name)+" "+str(last_name)
#         username=nlist[3]
#         status=nlist[4]
#         if status:
#             status="Active"
#         else:
#             status="Deactive"

#         user_info=models.UserProfile.objects.filter(user=user_id).values_list('user_type__name','district__district_name','state__state_name')
#         for i in user_info:
#             user_type=i[0]
#             district=i[1]
#             state=i[2]

#         count+=1
#         row.append(count)
#         row.append(user_type)
#         row.append(full_name)
#         row.append(username)
#         row.append(district)
#         row.append(state)
#         row.append(status)
#         data.append(row)

#     return render(request, 'manage_user.html', {'data':(data)})

# @csrf_exempt
# def get_manage_user(request):
#     data=[]
#     user_type=""
#     district=""
#     state=""
#     count=0
#     row=[]
#     user_info=models.UserProfile.objects.filter(~Q(user='1')).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
#     for i in user_info:
#         user_type=i[0]
#         district=i[1]
#         state=i[2]
#         user_id=i[3]
#         first_name=i[4]
#         last_name=i[5]
#         full_name=str(first_name)+" "+str(last_name)
#         username=i[6]
#         status=i[7]
#         if status:
#             status="Active"
#         else:
#             status="Deactive"


#         count+=1
#         data.append([count,str(user_type),str(full_name),str(username),str(district),str(state), str(status),"","","",user_id])
#     return render(request, 'manage_user.html', {'data':(data)})

@csrf_exempt
def get_manage_user(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(~Q(user='1')).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
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
        #user_id
        data.append([count,str(user_type),str(full_name),str(username),str(district),str(state), str(status),str(btn),"<a href='/edit_user/"+str(user_id)+"' class='btn'><i class='fas fa-edit'></i> Edit</a> | <a class='btn' href='/edit_user/"+str(user_id)+"'><i class='fas fa-eye'></i> View</a>"])
    return render(request, 'manage_user.html', {'data':(data)})


@csrf_exempt
def get_product(request):
    data=[]
    count=0
    product_info=models.Product.objects.all().values_list('product_image','product_name','product_code','product_unit','product_price','id')
    for i in product_info:
        product_image=i[0]
        product_name=i[1]
        product_code=i[2]
        product_unit=i[3]
        product_price=i[4]
        product_id=i[5]
        count+=1
        data.append([count,str(product_image),str(product_name),str(product_code),str(product_unit),str(product_price),'',product_id])
    return render(request, 'get_product.html', {'data':(data)})

@csrf_exempt
def add_product(request):
    print("Add USer")
    if request.method == 'POST':
        data={}
        product_image=''
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        product_unit = request.POST.get('product_unit')
        sub_code = request.POST.get('sub_code')
        product_unit1=product_unit+' '+sub_code
        product_price = request.POST.get('product_price')
        if request.FILES.get('product_image'):
            product_image = request.FILES['product_image']

        product = models.Product.objects.create(product_name=product_name,product_code=product_code,product_unit=product_unit,product_price=product_price,product_image=product_image)
        product.save()
        # data={'product_name':product_name,'product_unit':product_unit,"status":True}
        # return render(request, 'product.html', {})
        response=JsonResponse({'status':'success'})
        return response

    else:
        return render(request, 'product.html', {})

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
        print("user_typeuser_type",user_type)
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')

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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_retailer.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@csrf_exempt
def get_retailer(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=2).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
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
    return render(request, 'manage_retailer.html', {'data':(data)})


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
        print("user_typeuser_type",user_type)
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')

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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_retailer.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@csrf_exempt
def get_retailer(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=2).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
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
    return render(request, 'manage_retailer.html', {'data':(data)})


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
        user_type =3
        print("user_typeuser_type",user_type)
        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')

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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_farmer.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@csrf_exempt
def get_farmer(request):
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
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=0, language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id,soil_card=soil_card,land_area=land_area)
        userprofile.save()
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'add_wholesaler.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})

@csrf_exempt
def get_wholesaler(request):
    data=[]
    user_type=""
    district=""
    state=""
    count=0
    row=[]
    user_info=models.UserProfile.objects.filter(user_type=4).values_list('user_type__name','district__district_name','state__state_name','user','user__first_name','user__last_name','user__username','user__is_active')
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