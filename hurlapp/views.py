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
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
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
                response=JsonResponse({'status':'error','msg':'Your account was inactive'})
                return response
        else:
            response=JsonResponse({'status':'error','msg':'Invalid login details'})
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

        #user_photo = request.FILES['user_photo']
        #print("user_photo",user_photo)
        #hotel_image_view(request)
        #user_photo=request.FILES.get('user_photo')
        #file = request.FILES['user_photo']
        #print("user_photo",user_photo,file)
        #input()
        # save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['file'])
        # user_photo = default_storage.save(save_path, request.FILES['file'])
        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=0,email=email)
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
        print("saveee calll")
        response=JsonResponse({'status':'success'})
        return response

    else:
        MyProfileForm = forms.ProfileForm()
        return render(request, 'userprofile.html', {'group_data':group_data,"lang_data":lang_data,"state_data":state_data,'district_data':[{'id':'1','name':'Thane'}]})



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
        print(username)
        if status:
            status="Active"
        else:
            status="Deactive"


        count+=1
        data.append([count,str(user_type),str(full_name),str(username),str(district),str(state), str(status),"",user_id])
    return render(request, 'manage_user.html', {'data':(data)})



@csrf_exempt
def addProduct(request):
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
        return render(request, 'product.html', {})

    else:
        #return render(request, 'login.html', {})
        return render(request, 'product.html', {})

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



from hurlapp.forms import ProfileForm
from hurlapp.models import Hotel
import os 
def SaveProfile(request):
    saved = False 
    if request.method == "POST":
      print("request.POST",request.POST)
      print("request.POST",request.FILES)
      MyProfileForm = ProfileForm(request.POST, request.FILES)      
      if MyProfileForm.is_valid():
         print("valid")
         profile = models.Hotel()
         profile.name = MyProfileForm.cleaned_data["name"]
         profile.hotel_Main_Img = MyProfileForm.cleaned_data["picture"]
         profile.save()
         saved = True
         response=JsonResponse({'status':'success'})
         return response
      else:
          print("not Valid")

    else:
       MyProfileForm = forms.ProfileForm()
    return render(request, 'profile.html', {"group_data":get_group()})