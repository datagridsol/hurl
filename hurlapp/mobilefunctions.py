import math, random
from django.shortcuts import render
from hurlapp.forms import UserForm
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

@csrf_exempt
def login(request):
	if request.method == 'POST':
		mobile_number = request.POST.get('mobile_number')
		if User.objects.filter(username=mobile_number).exists():
			userprofile=models.UserProfile.objects.get(user__username=mobile_number)
			genotp=generateOTP()
			userprofile.otp = genotp
			userprofile.save()
			data={"mobile_number":mobile_number,"opt":genotp}
			response=JsonResponse({'status':'success','msg':'Opt Added Successfully','data':data})
			return response
		else:
			response=JsonResponse({'status':'error','msg':'Mobile Number Not Exits'})
			return response

@csrf_exempt
def check_login(request):
	if request.method == 'POST':
		mobile_number = request.POST.get('mobile_number')
		otp = request.POST.get('otp')
		userprofileDetails = models.UserProfile.objects.filter(Q(user__username=mobile_number) & Q(otp=otp)).values_list('user_type__name','user__first_name','user__last_name','user')
		if userprofileDetails:
			for i in userprofileDetails:
				user_type=i[0]
				first_name=i[1]
				last_name=i[2]
				user_id=i[3]
				full_name=first_name+" "+last_name
				data={"user_type":user_type,"name":full_name,"mobile_number":mobile_number,"otp":otp,"user_id":str(user_id)}
				response=JsonResponse({'status':'success','msg':'Otp Match','data':data})
				return response
		else:
			response=JsonResponse({'status':'error','msg':'Invalid Otp'})
			return response

# function to generate OTP 
def generateOTP() : 
    digits = "0123456789"
    OTP = "" 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
    return OTP 

@csrf_exempt
def get_wholesaler(request):
    whole_data=[]
    wholesaler_data=models.UserProfile.objects.filter(user_type=3).values_list('user','user__first_name','user__last_name','parent_id')
    for i in wholesaler_data:
        full_name=i[1]+' '+i[2]
        case1 = {'user_id': i[0], 'name': full_name}
        whole_data.append(case1)
    response=JsonResponse({'status':'success','data':whole_data})
    return response

def get_group():
    group_data=[]

    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    data={}
#    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
#    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])

#    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
#    if my_user_type:
#        print(my_user_type[0][0])

        case = {'id': i[0], 'name': i[1]}
        group_data.append(case)
    return group_data



#@login_required
#@csrf_exempt
def add_user_mobile(request):
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
#        if (' ' in full_name) == True:
#            full_name_split=full_name.split(' ')
#            if len(full_name_split)==2:
#                first_name=full_name_split[0]
#                last_name=full_name_split[1]
#            if len(full_name_split)==3:
#                first_name=full_name_split[0]
#                last_name=full_name_split[2]
#        else:
#            first_name=full_name
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
        response = JsonResponse({"status":"error"})
    return response


def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],}
        lang_data.append(case1)
    return lang_data


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
################################################################################

@csrf_exempt
def get_state_list(request):
    state_data=[]
    state_list=models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1]}
        state_data.append(case2)
    response=JsonResponse({'status':'success','data':state_data})
    return response

@csrf_exempt
def get_district_list(request):
    district_data=[]
    district_list=models.District.objects.all().values_list('id', 'district_name')
    for i in district_list:
        case2 = {'id': i[0], 'name': i[1]}
        district_data.append(case2)
    response=JsonResponse({'status':'success','district_data':district_data})
    return response

@csrf_exempt
def get_city_list(request):
    city_data=[]
    city_list=models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    response=JsonResponse({'status':'success','data':city_data})
    return response


@csrf_exempt
def all_manage_contain(request):
    data=[]
    list=models.ManageContent.objects.all().values_list('id', 'title_eng','title_hnd','date','state','district','group',
    'contains_eng','contains_hnd','user_id_admin_id','status','created_at','updated_at','feature_image')
    for i in list:
        case2 = {'id': i[0], 'title_eng': i[1], 'title_hnd': i[2],'date':i[3],'state':i[4],'district':i[5],'group':i[6],
        'contains_eng':i[7],'contains_hnd':i[8],'user_id_admin_id':i[9],'status':i[10],'created_at':i[11],'updated_at':i[12],
        'feature_image':i[13]}
        data.append(case2)
    response=JsonResponse({'status':'success','data':data})
    return response


@csrf_exempt
def get_product_mobile(request):
    data=[]
    count=0
    product_info=models.Product.objects.all().values_list('product_image','product_name','product_code','product_unit','product_unit_name','product_price','id','status')
    for i in product_info:
        product_image=i[0]
        product_name=i[1]
        product_code=i[2]
        product_unit=i[3]
        product_unit_name=i[4]
        product_price=i[5]
        product_id=i[6]
        status=i[7]
        count+=1
        case1 = {'product_id':product_id, 'product_name': product_name,'product_code':product_code,'product_unit':product_unit,'product_unit_name':product_unit_name,'product_price':product_price,'status':status}
        data.append(case1)
    response=JsonResponse({'status':'success','data':data})
    return response

@csrf_exempt
def get_username(request):
    username=request.POST.get('mobile_number')
    if User.objects.filter(username=username).exists():
        response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
        return response
    else:
        response=JsonResponse({'status':'success'})
        return response

@csrf_exempt
def get_farmer_list(request):
    farmer_data=[]
    username=request.POST.get('mobile_number')
    farmer_list=models.UserProfile.objects.filter(user_type=3,user__username=username).values_list('id', 'user__first_name','user__last_name')
    for i in farmer_list:
        first_name=i[1]
        last_name=i[2]
        full_name=first_name+' '+ last_name
        case2 = {'id': i[0], 'name': full_name}
        farmer_data.append(case2)
    response=JsonResponse({'status':'success','data':farmer_data})
    return response
    

@csrf_exempt
def add_order_list(request):
    # if request.user.groups.filter(name="admin").exists():
    #     print("in")
    # else:
    #     print ("out")
    if request.method == 'POST':
        data={}
        product_list = request.POST.get('product_list')
        total_price=request.POST.get('total_price') 
        user_id_farmer_id = request.POST.get('farmer_id')
        user_id_retailer_id = request.POST.get('retailer_id')
        product_quantity=request.POST.get('product_quantity')
        product_price=request.POST.get('product_price')
        product_total_price=request.POST.get('product_total_price')
        user_id_farmer_id=User.objects.get(id=user_id_farmer_id)
        user_id_retailer_id=User.objects.get(id=user_id_retailer_id)

        order_data= models.Order.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,total_price=total_price)
        order_data.save()
        new_order_id = order_data.id

        product_list = [{"id":"1","name":"Ferti"},{"id":"2","name":"Ammonium Sulphate"}] #[{"id":"1","name":"Ferti"},{"name":"Ammonium Sulphate","id":"2"}]
        for product in product_list:
            product_id=product['id']
            product_name=product['name']
            product_id=models.Product.objects.get(id=product_id)
            new_order_id=models.Order.objects.get(id=new_order_id)
            product_order_data= models.OrderProductsDetail.objects.create(product=product_id,order=new_order_id,product_quantity=product_quantity,product_price=product_price,product_total_price=product_total_price)
        product_order_data.save()
        loyalty_data= models.LoyaltyPoints.objects.filter(loyalty_type='Order').values_list('id', 'loyalty_point')
        for i in loyalty_data:
            loyalty_point=i[1]
        user_loyalty_data= models.UserLoyaltyPoints.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,from_user_id=user_id_retailer_id,order_id=new_order_id,loyalty_point=loyalty_point)
        user_loyalty_data.save()
        data={'order_id':new_order_id,"status":True}
    response=JsonResponse({'status':'success','msg':'Order Placed Successfully','data':data})
    return response
