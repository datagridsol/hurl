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

@csrf_exempt
def add_user_mobile(request):
    gr_no=[]

    first_name=''
    last_name=''
    city_name=''
    fertilizer_photo=''
    print(request.user.id)
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
    if my_user_type:
        print(my_user_type[0][0])

    if request.method == 'POST':
        data={}
        full_name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        username = request.POST.get('mobile_number')
        password = request.POST.get('mobile_number')
        state=request.POST.get('state')
        city=request.POST.get('city')
        district=request.POST.get('district')
        pincode=request.POST.get('pincode')
        address=request.POST.get('address')
        aadhar_no=request.POST.get('aadhar_no')
        langn_id=request.POST.get('language_id')
        aadhar_card=request.POST.get('aadhar_card')
        user_photo=request.POST.get('user_photo')
        fertilizer_photo=request.POST.get('fertilizer_photo')
        wholesaler_id=request.POST.get('wholesaler_id')
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

        if request.POST.get('user_type'):
        	user_type=request.POST.get('user_type')
        else:
        	user_type="2"

       	
        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,is_active=0,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id1=models.Language.objects.get(id=langn_id)
        state1=models.State.objects.get(id=state)
        district1=models.District.objects.get(id=district)
        if city:
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=wholesaler_id,company_name=company_name,language=langn_id1,aadhar_no=aadhar_no,state=state1,city=city_name,district=district1,pincode=pincode,address=address,user_photo=user_photo,aadhar_card=aadhar_card,fertilizer_photo=fertilizer_photo)
        userprofile.save()
        data={"user_id":new_Uid,"name":full_name,"company_name":company_name,"mobile_number":username,"email":email,"language":langn_id,"aadhar_no":aadhar_no,"state":state,"city":city_name,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"fertilizer_photo":fertilizer_photo}
        response=JsonResponse({'status':'success','data':data})
        return response


@csrf_exempt
def get_product_mobile(request):
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
        case1 = {'product_id':product_id, 'product_name': product_name,'product_code':product_code,'product_unit':product_unit,'product_unit':product_unit,'product_price':product_price}
        data.append(case1)
    response=JsonResponse({'status':'success','data':data})
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
def add_contain(request):
        gr_no=[]
        contain=[]
#        user=get_user()
#        group_data=get_group()
#        lang_data=get_langauge()
#        state_data=get_state()
#        city_data=get_city()
#        users=auth_user()
        user_type=Group.objects.all().values_list('id', 'name')
        for i in user_type:
            gr_no.append(i[1])
        my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
        if my_user_type:
            pass
        if request.method == 'POST':
            title_eng = request.POST.get('title_eng')
            title_hnd = request.POST.get('title_hnd')
            date = request.POST.get('datetime.datetime.now()')
            state=request.POST.get('state')
            district=request.POST.get('district')
#            user_type=Group.objects.all().values_list('id', 'name')
            user = request.POST.get('user')
#            if Group.filter(user_type=name).exists():
#                users = auth_user.objects.filter(username=username)
#            else:
#                users = auth_user.objects.all()

            new_contain = request.POST.get('News_contain')
            contain = models.ManageContent.objects.create(title_eng=title_eng,title_hnd=title_hnd,date=date,
            state=state,district=district,new_contain=new_contain,user=user)
            contain.save()

#            contain = {'title_eng'=title_eng,'title_hnd'=title_hnd,'date'=date,
#            'state'=state,'district'=district,'user_type'=user_type,'new_contain'=new_contain,'users'=users}

            response=JsonResponse({'status':'success','contain':contain})
            return response

        else:
            return JsonResponse({'status':'Error'})
