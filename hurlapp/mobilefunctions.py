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
from operator import itemgetter
from datetime import datetime

# For login
@csrf_exempt
def login(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        if User.objects.filter(username=mobile_number).exists():
            if User.objects.filter(username=mobile_number,is_active=1).exists():
                userprofile=models.UserProfile.objects.get(user__username=mobile_number)
                genotp=generateOTP(mobile_number)
                userprofile.otp = genotp
                userprofile.save()
                data={"mobile_number":mobile_number,"opt":genotp}
                response=JsonResponse({'status':'success','msg':'OTP Sent Successfully','data':data})
                return response
            else:
                response=JsonResponse({'status':'error','msg':'Your account is not approved by admin'})
                return response
        else:
            response=JsonResponse({'status':'error','msg':'Mobile Number Not Exist'})
            return response


# For check_login
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
@csrf_exempt
# def generateOTP() : 
#     digits = "0123456789"
#     OTP = "123" 
# #    for i in range(4) : 
# #        OTP += digits[math.floor(random.random() * 10)] 
#     return OTP

# function to generate OTP
@csrf_exempt
def generateOTP(mobile_number) :
   import requests
   digits = "0123456789"
   OTP = random.randint(1000,9999)
   Phone_number=mobile_number
   sms_url="http://sms.peakpoint.co/sendsmsv2.asp"
   #data = {"user":"datagrid","password":"Dat$Fagt&","sender":"DATAGR","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":"Otp For Login"+" "+str(OTP)}
   
   data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":str(OTP)+" "+"is your OTP, use this to login to your Apna Urea App."}
   requests.packages.urllib3.disable_warnings()
   r = requests.post(sms_url,data = data)
   response=JsonResponse({'status':'success','msg':'Otp Match','data':str(r.content)})
   return OTP

# For get_wholesaler
@csrf_exempt
def get_wholesaler_mobile(request):
    whole_data=[]
    wholesaler_data=models.UserProfile.objects.filter(user_type=4).values_list('user','user__first_name','user__last_name','parent_id')
    for i in wholesaler_data:
        full_name=i[1]+' '+i[2]
        case1 = {'user_id': i[0], 'name': full_name}
        whole_data.append(case1)
    response=JsonResponse({'status':'success','data':whole_data})
    return response

# For user_status
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

# For get_username
def get_username(request):
    username=request.POST.get('username')
    if User.objects.filter(username=username).exists():
        response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
        return response
    else:
        response=JsonResponse({'status':'success'})
        return response

# For user_status
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

# For get_langauge
@csrf_exempt
def get_langauge():
    lang_data=[]
    lang_type=models.Language.objects.all().values_list('id', 'lang_name')
    for i in lang_type:
        case1 = {'id': i[0], 'name': i[1],}
        lang_data.append(case1)
    return lang_data

# For get_group
@csrf_exempt
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

# For Get_state
@csrf_exempt
def get_state():
    state_data=[]
    state_list=models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name': i[1].capitalize()}
        state_data.append(case2)
    state_data=sorted(state_data, key=itemgetter('name'))
    return state_data

# For get_district
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


#For Getting city name
@csrf_exempt
def get_city():
    city_data=[]
    city_list=models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    return city_data

# For Adding user from mobile
@csrf_exempt
def add_user_mobile(request):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    user_photo=''
    aadhar_card=''
    city=''
    pan_card=''
    vote_id=''
    soil_card=''
    vote_card=''
    land_area=''
    pincode=0
    address=''
    gst_photo=''
    fertilizer_photo=''
    fms_id=''
    fertilizer_licence=''
    gst_number=''
    group_data=get_group()
    lang_data=get_langauge()
    state_data=get_state()
    city_data=get_city()
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])
#    my_user_type=Group.objects.filter(user=request.user.id).values_list('name','id')
#    if my_user_type:
#        print(my_user_type[0][0])
    if request.method == 'POST':
        data={}
        status=1
        username = request.POST.get('mobile_number')
        if User.objects.filter(username=username).exists():
            response=JsonResponse({'status':'error','msg':'Phone No Already exists'})
            return response
        password = request.POST.get('mobile_number')
        company_name = request.POST.get('company_name')
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
#        user_type = request.POST.get('user_type')
        if request.POST.get('user_type'):
            user_type=request.POST.get('user_type')
            sendwlcomeFarmer(username,full_name)
        else:
            user_type="2"
            status=0

        if request.POST.get('fms_id'):
            fms_id=request.POST.get('fms_id')
        if request.POST.get('fertilizer_licence'):
            fertilizer_licence=request.POST.get('fertilizer_licence')
        if request.POST.get('gst_number'):
            gst_number=request.POST.get('gst_number')
        

        aadhar_no=request.POST.get('aadhar_no')
        state=request.POST.get('state')
        if request.POST.get('city'):
            city=request.POST.get('city')
        district=request.POST.get('district')
        if request.POST.get('pincode'):
            pincode=request.POST.get('pincode')
        if request.POST.get('address'):
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
        if request.FILES.get('fertilizer_photo'):
            fertilizer_photo = request.FILES['fertilizer_photo']

        if request.FILES.get('land_area'):
            land_area=request.POST.get('land_area')

        if request.FILES.get('gst_photo'):
            gst_photo = request.FILES['gst_photo']
        if request.POST.get('retailer_id'):
            parent_id=request.POST.get('retailer_id')
        else:
            parent_id=0

        new_user = User.objects.create(username = username,password = username,first_name=first_name,last_name=last_name,is_active=status,email=email)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id

        if request.POST.get('wholesaler_id'):
            listdata=request.POST.get('wholesaler_id')
            x=listdata.split(",")
            for i in x:
                wholesaler_id=i
                user_id_whole=User.objects.get(id=wholesaler_id)
                print('user_id_whole=> ',user_id_whole)
                user_link_data= models.UserLinkage.objects.create(retailer_user_id=new_user,wholesaler_user_id=user_id_whole)
                print('wholesaler_id=> ',wholesaler_id)
                user_link_data.save()

        user_type=Group.objects.get(id=user_type)
        user_type.user_set.add(new_Uid)
        langn_id=models.Language.objects.get(id=langn_id)
        state=models.State.objects.get(id=state)
        district=models.District.objects.get(id=district)
        if city != '':
            if models.City.objects.filter(city_name=city).exists():
                city_name=city
            else:
                new_city = models.City.objects.create(city_name =city,status=1)
                new_city.save()
                city_name=new_city.city_name
        print('new_Uid => '+str(new_Uid))
        print('user_type => '+str(user_type))
        print('parent_id => '+str(parent_id))
        print('langn_id => '+str(langn_id))
        print('aadhar_no => '+str(aadhar_no))
        print('state => '+str(state))
        print('city_name => '+str(city_name))
        print('district => '+str(district))
        print('pincode => '+str(pincode))
        print('address => '+str(address))
        print('user_photo => '+str(user_photo))
        print('fertilizer_photo => '+str(fertilizer_photo))
        print('soil_card => '+str(soil_card))
        print('land_area => '+str(land_area))
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type=user_type,parent_id=parent_id,language=langn_id,aadhar_no=aadhar_no,state=state,city=city_name,district=district,pincode=pincode,address=address,user_photo=user_photo,fertilizer_photo=fertilizer_photo,soil_card=soil_card,land_area=land_area,gst_photo=gst_photo,fms_id=fms_id,fertilizer_licence=fertilizer_licence,gst_number=gst_number,company_name=company_name,aadhar_card=aadhar_card,pan_card=pan_card,vote_id=vote_id)
        userprofile.save()
        response=JsonResponse({'status':'success','msg':'User registered successfuly'})
        return response

    else:
        response=JsonResponse({'status':'error','msg':'Something went wrong. Please try again.'})
        return response

@login_required
@csrf_exempt
def add_farmer_mobile(request):
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
        user_type =3
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

        new_user = User.objects.create(username = username,password = password,first_name=first_name,last_name=last_name,
        is_active=1,email=email)
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
        response=JsonResponse({'status':'error'})
        return response

#@login_required
@csrf_exempt
def get_farmer_mobile(request):
    user_id = request.POST.get('user_type')
    data=[]
    district=""
    state=""
    whole_data=[]
    count=0
    row=[]
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    company_name=''
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

    user_info=models.UserProfile.objects.filter(user=user_id).values_list('user_type__name','language__lang_name','user__first_name','user__last_name','user__email','user__username','aadhar_no','state__state_name','city','district__district_name','pincode','address','user_photo','aadhar_card','pan_card','vote_id','soil_card','land_area','user_type__id','language__id','state__id','district__id','gst_number','fertilizer_licence','fms_id','gst_photo','fertilizer_photo','company_name')
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
            company_name=i[27]
            wholesaler_data=models.UserLinkage.objects.filter(retailer_user_id=user_id).values_list('wholesaler_user_id__id')
            if wholesaler_data:
               for i in wholesaler_data:
                   #whole_data=str(i[0])+','+str(whole_data)
                   whole_data.append(i[0])
            user_type={"name":user_type[0],'id':group_id}
            language={"name":language,'id':lang_id}
            state={"name":state,'id':state_id}
            district={"name":district,'id':district_id}
    	    
            data={"user_type":user_type,"language":language,"full_name":full_name,"email":email,"mobile_number":mobile_number,"aadhar_no":aadhar_no,"state":state,"city":city,"district":district,"pincode":pincode,"address":address,"user_photo":user_photo,"aadhar_card":aadhar_card,"pan_card":pan_card,"vote_id":vote_id,"soil_card":soil_card,"land_area":land_area,'group_data':group_data,"lang_data":lang_data,"state_data":state_data,"gst_number":gst_number,"fertilizer_licence":fertilizer_licence,"fms_id":fms_id,"gst_photo":gst_photo,"fertilizer_photo":fertilizer_photo,"company_name":company_name,"wholesaler_data":whole_data}
    response=JsonResponse({'status':'success','data':data})
    return response

@csrf_exempt
def save_farmer_mobile(request):
    gr_no=[]
    first_name=''
    last_name=''
    city_name=''
    state=''
    fms_id=''
    fertilizer_licence=''
    gst_number=''
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
    user_type = request.POST.get('user_type')
    user_id = request.POST.get('user_id')
    password = request.POST.get('mobile_number')
    company_name = request.POST.get('company_name')
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
    if request.POST.get('fms_id'):
    	fms_id=request.POST.get('fms_id')
    if request.POST.get('fertilizer_licence'):
    	fertilizer_licence=request.POST.get('fertilizer_licence')
    if request.POST.get('gst_number'):
    	gst_number=request.POST.get('gst_number')
    user_info_photo=models.UserProfile.objects.filter(user=user_id).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card')
    for i in user_info_photo:
        user_photo1=i[0],
        aadhar_card1=i[1]
        pan_card1=i[2]
        vote_id1=i[3]
        soil_card1=i[4]
    user_info_photo=list(models.UserProfile.objects.filter(user=user_id).values_list('user_photo','aadhar_card','pan_card','vote_id','soil_card'))
    for i in user_info_photo:
        user_photo1=i[0],
        aadhar_card1=i[1]
        pan_card1=i[2]
        vote_id1=i[3]
        soil_card1=i[4]
    user_profile = models.UserProfile.objects.get(user=user_id)
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
    	fertilizer_photo = request.FILES['fertilizer_photo']
    	user_profile.fertilizer_photo = fertilizer_photo



    if request.FILES.get('gst_photo'):
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
    
    #user_profile.parent_id=0
    user_profile.company_name=company_name
    user_profile.language=langn_id
    #user_profile.aadhar_no=aadhar_no
    user_profile.state=state
    user_profile.city_name=city_name
    user_profile.district=district
    user_profile.pincode=pincode
    user_profile.address=address
    user_profile.land_area=land_area
    
    user_profile.save()


    if request.POST.get('wholesaler_id'):
        models.UserLinkage.objects.filter(retailer_user_id=user_id).delete()
        user_int=User.objects.get(id=user_id)
        listdata=request.POST.get('wholesaler_id')
        x=listdata.split(",")
        for i in x:
            wholesaler_id=i
            user_id_whole=User.objects.get(id=wholesaler_id)
            print('user_id_whole=> ',user_id_whole)
            user_link_data= models.UserLinkage.objects.create(retailer_user_id=user_int,wholesaler_user_id=user_id_whole)
            print('wholesaler_id=> ',wholesaler_id)
            user_link_data.save()

    response=JsonResponse({'status':'success','msg':'Profile Updated Successfuly'})
    return response

@csrf_exempt
def get_farmer_profile(request):

	user_type = request.POST.get('user_type')
	userprofileDetails = models.UserProfile.objects.filter(user_type=user_type).values_list('user')
	for i in userprofileDetails:
		user_type=i[0]
		data={"user_type":user_type,}
        # "name":full_name,"mobile_number":mobile_number,"otp":otp,"user_id":str(user_id)}
		response=JsonResponse({'status':'success','msg':'Otp Match','data':data})
		return response


# @login_required
# @csrf_exempt
# def get_farmer_id(request):
#     data=[]
#     user_type=""
#     district=""
#     state=""
#     count=0
#     row=[]
#     user_type = request.POST.get('user_type')
#     user_info=models.UserProfile.objects.filter(user_type=user_type).values_list('user_type__name',
#     'user__username',
#     'user',
#     'user_type').order_by('-created_at')
#     for i in user_info:

#         user_id=i[0]

#         username=i[1]
#         user_type = i[2]
#         count+=1
#         data.append([count,str(username),str(user_id),str(user_type)])
#     response = JsonResponse({'success':'success','data':(data)})

#         return response


@login_required
@csrf_exempt
def edit_farmer_mobile(request, pk):
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
            response= JsonResponse({'status':'not change',"data":data})
            return response

#@login_required
@csrf_exempt
def search_farmer(request):
    username = request.POST.get('mobile_number')
    case = []
    if User.objects.filter(username=username).exists():
        data = User.objects.filter(username=username).values_list('id','first_name','last_name')
        for ele in data:
            data = {'id':ele[0],'first_name':ele[1],'last_name':ele[2]}
            case.append([str(data)])
            response=JsonResponse({'data':data,'msg': "welcome",'status': "success"})
            return response

 

    else:
        response=JsonResponse({'status':'Farmer Not Registered'})
        return response


# For Getting State list
@csrf_exempt
def get_state_list(request):
    state_data=[]
    state_list=models.State.objects.all().values_list('id', 'state_name')
    for i in state_list:
        case2 = {'id': i[0], 'name':i[1].capitalize()}
        state_data.append(case2)
    state_data=sorted(state_data, key=itemgetter('name'))
    response=JsonResponse({'status':'success','data':state_data})
    return response

# For Getting District list
@csrf_exempt
def get_district_list(request):
    district_data=[]
    state_id=request.POST.get('state_id')
    district_list=models.District.objects.filter(state_id=state_id).values_list('id', 'district_name')
    for i in district_list:
        case2 = {'id': i[0], 'name': i[1]}
        district_data.append(case2)
    district_data=sorted(district_data, key=itemgetter('name'))
    response=JsonResponse({'status':'success','district_data':district_data})
    return response


# For Getting City list
@csrf_exempt
def get_city_list(request):
    city_data=[]
    city_list=models.City.objects.all().values_list('id', 'city_name')
    for i in city_list:
        case2 = {'id': i[0], 'name': i[1]}
        city_data.append(case2)
    response=JsonResponse({'status':'success','data':city_data})
    return response

# For Getting all_manage_contain
@csrf_exempt
def all_manage_contain(request):
    user_type=request.POST.get('user_type')
    data=[]
    my_user_type=Group.objects.filter(name=user_type).values_list('name','id')
    if my_user_type:
        user_id=my_user_type[0][1]
    list=models.ManageContent.objects.filter(group_id__contains=user_id).values_list('id', 'title_eng','title_hnd','date','state_id','district_id','group_id',
    'contains_eng','contains_hnd','user_id_admin_id','status','created_at','updated_at','feature_image')
    for i in list:
        district=i[5]
        if district != 0:
            district=models.District.objects.get(id=district)
        else:
            district=""
        state=i[4]
        if state != 0:
            state=models.State.objects.get(id=state)
        else:
            state=""
        case2 = {'id': i[0], 'title_eng': i[1], 'title_hnd': i[2],'date':i[3],'state':str(state),'district':str(district),'group':i[6],
        'contains_eng':i[7],'contains_hnd':i[8],'user_id_admin_id':i[9],'status':i[10],'created_at':i[11],'updated_at':i[12],
        'feature_image':i[13]}
        data.append(case2)
    response=JsonResponse({'status':'success','data':data})
    return response

@csrf_exempt
def get_product_mo(request):
    product_list = []
    product_details = models.Product.objects.all().values_list('id','product_name','product_price')
    for i in product_details:
        case1 = {'id': i[0], 'product_name': i[1], 'product_price': i[2]}
        product_list.append(case1)
    response=JsonResponse({'status':'success','data':product_list})
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
def get_price(request):
    if request.method == 'POST':
        product_data=[]
        product_id=request.POST.get('id')
        price_list=models.Product.objects.filter(id=product_id).values_list('id', 'product_price')
        for i in price_list:
            case2 = {'id': i[0], 'product_price': i[1]}
            product_data.append(case2)
        response=JsonResponse({'status':'success','price':product_data})
        return response

# For placing  order from mobile
@csrf_exempt
# def mobile_place_order(request):
#     if request.method == 'POST':
#         # products=get_product()
#         # price = get_price()
#         farmer_id = request.POST.get('farmer_id')
#         print(farmer_id)
#         retailer_id=request.POST.get('retailer_id')
#         # product_price=request.POST.get('price')
#         # product_quantity=request.POST.get('quantity')
#         total_price=request.POST.get('grand_total')

#         userprofile = models.Order.objects.create(user_id_farmer_id=farmer_id,
#         user_id_retailer_id=retailer_id,
#         # product_price=product_price,
#         # product_quantity=product_quantity,
#         total_price=total_price)
#         userprofile.save()
#         response=JsonResponse({'status':'success'})
#         return response
#     else:
#         response=JsonResponse({'status':'error'})
#         return response

@csrf_exempt
def mobile_place_order(request):
   # if request.user.groups.filter(name="admin").exists():
   #     print("in")
   # else:
   #     print ("out")
   list_id=[]
   if request.method == 'POST':
       data={}
       product_list = request.POST.get('product_list')
       product_list1=json.loads(product_list)
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
       list_id.append(new_order_id)
       for product in product_list1:
           product_id=product['id']
           product_name=product['name']
           print("product_id",product_id,list_id)
           product_id=models.Product.objects.get(id=product_id)
           new_order_id=models.Order.objects.get(id__in=list_id)
           print("new_order_id",new_order_id)
           product_order_data= models.OrderProductsDetail.objects.create(product=product_id,order=new_order_id,product_quantity=product_quantity,product_price=product_price,product_total_price=product_total_price)
           product_order_data.save()
       loyalty_data= models.LoyaltyPoints.objects.filter(loyalty_type='Order').values_list('id', 'loyalty_point')
       for i in loyalty_data:
           loyalty_id=i[0]
           loyalty_point=i[1]
       # print("loyalty_id",loyalty_id,loyalty_point)
       # user_loyalty_data= models.UserLoyaltyPoints.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,order_id=int(new_order_id),loyalty_points_id=str(loyalty_id),loyalty_point=int(loyalty_point),to_user_id=1,from_user_id=1,loyalty_type="Order")
       # user_loyalty_data.save()
       data={'order_id':loyalty_id,"status":True}

#     order = models.Product.objects.all().values_list('product_name','product_unit','product_price')
#     quanties=request.POST.get('quantity')
#     quantity = (quanties)
#     for ele in order:
#         product_name = ele[0]
#         product_unit = ele[1]
#         product_prices = ele[2]
#         product_price = float(product_prices)
#         grand_total=request.POST.get('grand_total')

#         # sub_total = float(product_price) * (quantity)
#         # grand_total = 0
#         # for cost in sub_total:
#         #     grand_total = grand_total + float(cost)

#     order_place = models.OrderProductsDetail.objects.create(
#         product_name=product_name,
#         product_unit=product_unit,
#         quantity=quantity,
#         product_price=product_price,
#         grand_total=grand_total
#         )
#     order_place.save()
#     #data={'product_name':product_name,'product_unit':product_unit,"status":True}

#   # response = JsonResponse({"status":"success",'product_name':product_name,'product_unit':product_unit,"quantity":quantity,"product_price":product_price,
#     "grand_total":grand_total,"status":True})
#     return response

# For Getting product list

# @csrf_exempt
# def get_product_mobile(request):
#     data=[]
#     count=0
#     product_info=models.Product.objects.all().values_list('product_image','product_name','product_code','product_unit','product_price','id')
#     for i in product_info:
#         product_image=i[0]
#         product_name=i[1]
#         product_code=i[2]
#         product_unit=i[3]
#         product_price=i[4]
#         product_id=i[5]
#         count+=1
#         case1 = {'product_id':product_id, 'product_name': product_name,'product_code':product_code,'product_unit':product_unit,'product_unit':product_unit,'product_price':product_price}
#         data.append(case1)
#     response=JsonResponse({'status':'success','data':data})
#     return response

# For Add product
@csrf_exempt
def add_product_mobile(request):
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
        response=JsonResponse({'status':'success'})
        return response

    else:
        response=JsonResponse({'status':'error'})
        return response


@login_required
@csrf_exempt
def get_user_mobile(request):
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
        data.append([count,str(user_type),str(full_name),str(username),str(district),str(state), str(status),str(user_id)])
        response = ({'data':(data)})
        return response

@csrf_exempt
def add_order_list(request):
    # if request.user.groups.filter(name="admin").exists():
    #     print("in")
    # else:
    #     print ("out")
    list_id=[]
    recharge_amount= random.randint(50,999)
    if request.method == 'POST':
        data={}
        product_list = request.POST.get('product_list')
        product_list1=json.loads(product_list)
        total_price=request.POST.get('grand_total') 
        user_id_farmer_id = request.POST.get('farmer_id')
        user_id_retailer_id = request.POST.get('retailer_id')
        user_id_farmer_id=User.objects.get(id=user_id_farmer_id)
        user_id_retailer_id=User.objects.get(id=user_id_retailer_id)

        order_data= models.Order.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,total_price=total_price,created_at=datetime.now())
        order_data.save()
        new_order_id = order_data.id
        list_id.append(new_order_id)
        for product in product_list1:
            product_id=product['id']
            #product_name=product['name']
            product_price=product['product_price']
            product_quantity=product['quantity']
            product_total_price=product['subtotal']
            product_id=models.Product.objects.get(id=product_id)
            new_order_id=models.Order.objects.get(id__in=list_id)
           
            product_order_data= models.OrderProductsDetail.objects.create(product=product_id,order=new_order_id,product_quantity=product_quantity,product_price=product_price,product_total_price=product_total_price)
            product_order_data.save()
        loyalty_data= models.LoyaltyPoints.objects.filter(loyalty_type='Order').values_list('id', 'loyalty_point')
        for i in loyalty_data:
            loyalty_id=i[0]
            loyalty_point=i[1]
        user_loyalty_data= models.UserLoyaltyPoints.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,order_id=int(list_id[0]),loyalty_points_id=str(loyalty_id),loyalty_point=int(loyalty_point),to_user_id=1,from_user_id=1,loyalty_type='Order')
        user_loyalty_data.save()
        user_recharge_data= models.Recharge.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,amount=int(recharge_amount),order=new_order_id,transation_id=0,transation_request='dummy',transation_response='dummy')
        user_recharge_data.save()
        recharge_id=user_recharge_data.id

        user_scratch_data= models.Scratch.objects.create(user_id_farmer_id=user_id_farmer_id,user_id_retailer_id=user_id_retailer_id,amount=int(recharge_amount),order=new_order_id)
        user_scratch_data.save()
        # mobile_number=User.objects.get(id=user_id_farmer_id).values_list('username')
        # mobile_number=mobile_number[0][0]
        # send_sms_order_placed(mobile_number)
        
        data={'recharge_id':recharge_id,'recharge_amount':recharge_amount,"status":True}
        response=JsonResponse({'status':'success','msg':'Order Placed Successfully','data':data})
        return response

@csrf_exempt
def get_farmer_list(request):
    farmer_data=[]
    username=request.POST.get('mobile_number')
    farmer_list=models.UserProfile.objects.filter(user_type=3,user__username=username).values_list('user__id', 'user__first_name','user__last_name')
    for i in farmer_list:
        first_name=i[1]
        last_name=i[2]
        full_name=first_name+' '+ last_name
        case2 = {'id': i[0], 'name': full_name}
        farmer_data.append(case2)
    response=JsonResponse({'status':'success','data':farmer_data})
    return response


# @csrf_exempt
# def get_reatiler_farmer_list(request):
#     farmer_data=[]
#     user_id=request.POST.get('user_id')
#     farmer_list=models.UserProfile.objects.filter(parent_id=user_id).values_list('user__id', 'user__first_name','user__last_name','user_photo')
#     for i in farmer_list:
#         first_name=i[1]
#         last_name=i[2]
#         full_name=first_name+' '+ last_name
#         user_photo=i[3]
#         case2 = {'id': i[0], 'name': full_name}
#         farmer_data.append(case2)
#     response=JsonResponse({'status':'success','data':farmer_data})
#     return response

@csrf_exempt
def get_reatiler_farmer_list(request):
    farmer_data=[]
    user_photo="/media/default/placeholder.png"
    user_id=request.POST.get('user_id')
    farmer_list=models.UserProfile.objects.filter(parent_id=user_id).values_list('user__id', 'user__first_name','user__last_name','user_photo')
    for i in farmer_list:
        first_name=i[1]
        last_name=i[2]
        full_name=first_name+' '+ last_name
        user_photo1=i[3]
        if user_photo1:
            user_photo=user_photo1
        case2 = {'id': i[0], 'name': full_name,"user_photo":user_photo}
        farmer_data.append(case2)
    response=JsonResponse({'status':'success','data':farmer_data})
    return response


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
def recharge_done(request):
    if request.method == 'POST':
        recharge_id = request.POST.get('recharge_id')
        user_recharge=models.Recharge.objects.get(id=recharge_id)
        user_recharge.status = 1
        user_recharge.updated_at=datetime.now()
        user_recharge.save()
        response=JsonResponse({'status':'success','msg':'Reacharge Done Successfully'})
        return response

@csrf_exempt
def send_opt_farmer(request):
    mobile_number = request.POST.get('mobile_number')
    genotp=sendoptFarmer(mobile_number)
    data={"mobilesendoptFarmer_number":mobile_number,"opt":genotp}
    response=JsonResponse({'status':'success','msg':'OTP sent Successfully','data':data})
    return response

@csrf_exempt
def sendoptFarmer(mobile_number):
   import requests
   digits = "0123456789"
   OTP = random.randint(1000,9999)
   Phone_number=mobile_number
   #Phone_number = request.POST.get('mobile_number')
   sms_url="http://sms.peakpoint.co/sendsmsv2.asp"
   data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":str(OTP)+" "+"is your OTP, use this to verify your mobile number for Apna Urea App"}
   requests.packages.urllib3.disable_warnings()
   r = requests.post(sms_url,data = data)
   response=JsonResponse({'status':'success','msg':'Otp Match','data':str(r.content)})
   return OTP


@csrf_exempt
def sendwlcomeFarmer(mobile_number,full_name) :
   import requests
   digits = "0123456789"
   OTP = random.randint(1000,9999)
   # Phone_number=mobile_number
   Phone_number = mobile_number
   full_name=full_name
   sms_url="http://sms.peakpoint.co/sendsmsv2.asp"
   data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":"Hello "+full_name+",Congratulations! You have successfully registered to Apna Urea App. You can login using the mobile number "+Phone_number+""}
   requests.packages.urllib3.disable_warnings()
   r = requests.post(sms_url,data = data)
   return OTP

@csrf_exempt
def send_sms_order_placed(mobile_number) :
   import requests
   digits = "0123456789"
   OTP = random.randint(1000,9999)
   Phone_number = mobile_number
   sms_url="http://sms.peakpoint.co/sendsmsv2.asp"
   data = {"user":"apnaurea","password":"apna#241","sender":"HURLSE","PhoneNumber":Phone_number,"sendercdma":"919860609000","text":"Your Order Placed Successfully"}
   requests.packages.urllib3.disable_warnings()
   r = requests.post(sms_url,data = data)
   return OTP

@csrf_exempt
def farmer_recharge_details(request):
   data=[]
   retailers_data=[]
   products_data=[]
   products_id=''
   state_data=get_state()
   recharge_status=''
   count=0
   request
   user_id = request.POST.get('user_id')
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

           else:
               recharge_status="Pending"

       count+=1
       data.append({'name':str(farmer__first_name)+' '+str(farmer_last_name),'order_id':str(order_id),"total_price":str(total_price),"reward_amount":str(amount),'recharge_status':recharge_status,'created_at':str(formatedDate)})
   response=JsonResponse({'status':'success','msg':'Recharge Details','data':data})
   return response


@csrf_exempt
def get_order_list(request):
   from django.db.models import Q
   data=[]
   retailers_data=[]
   products_data=[]
   products_id=''
   state_data=get_state()
   recharge_status=''
   count=0
   user_id = request.POST.get('user_id')
   my_user_type=Group.objects.filter(user=user_id).values_list('name','id')
   if my_user_type:
      user_type=my_user_type[0][1]

   if my_user_type:
       q = Q()
       if user_type==2:
           q &= Q(user_id_retailer_id=user_id)
           first_name='user_id_retailer_id__first_name'
           last_name='user_id_retailer_id__last_name'
       if user_type==3:
           q &= Q(user_id_farmer_id=user_id)
           first_name='user_id_farmer_id__first_name'
           last_name='user_id_farmer_id__last_name'

       user_info1=models.Order.objects.filter(q).values_list('id',str(first_name),str(last_name),'created_at','total_price').order_by('-updated_at')
       if user_info1:
           for i in user_info1:
               id=i[0]
               first_name=i[1]
               last_name=i[2]
               created_at=i[3]
               formatedDate = created_at.strftime("%d/%m/%Y")
               total_price=i[4]
               count+=1
               data.append({'name':str(first_name)+' '+str(last_name),"total_price":str(total_price),'created_at':str(formatedDate),'order_id':id})
           response=JsonResponse({'status':'success','msg':'All Order List','data':data})
       else:
           response=JsonResponse({'status':'success','msg':'No Order Details Found','data':[]})
   else:
       response=JsonResponse({'status':'success','msg':'No User Details Found','data':[]})

   return response



@csrf_exempt
def order_details_list(request):
    data=[]
    data_prod=[]
    count=0
    order_id = request.POST.get('order_id')
    order_info=models.Order.objects.filter(id=order_id).values_list('user_id_farmer_id__first_name','user_id_farmer_id__last_name','user_id_retailer_id__first_name','user_id_retailer_id__last_name','created_at','user_id_farmer_id__userprofile__state__state_name','user_id_farmer_id__userprofile__district__district_name','total_price','id','user_id_retailer_id__userprofile__address','user_id_farmer_id__username')

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
    od_id=order_info[0][8]
    address=order_info[0][9]
    phone=order_info[0][10]

    product_image="/media/default/placeholder.png"
    order_details=models.OrderProductsDetail.objects.filter(order_id=order_id).values_list('product_id','product_price','product_quantity','product_total_price','product__product_name','product__product_image','product__product_unit')
    
    for i in order_details:
        product_id=i[0]
        product_price=i[1]
        product_quantity=i[2]
        product_total_price=i[3]
        product_name=i[4]
        if i[5]!= "":
            product_image=i[5]
        product_unit=i[6]
        count+=1
        data.append([count,str(product_image),str(product_name),str(product_quantity)+' '+str(product_unit),str(product_price),str(product_total_price)])
        data_prod.append({"count":count,"product_image":str(product_image),"product_quantity":str(product_quantity)+' '+str(product_unit),"products_price":str(product_total_price),"products_total_price":str(product_total_price)})
    
    data={'full_name':full_name,'created_at':formatedDate,'state':state,'district':district,'amount':amount,'order_id':order_id,'address':address,'phone':phone,'data_prod':data_prod}
    response=JsonResponse({'status':'success','msg':'Order Datails','data':data})
    return response



@csrf_exempt
def get_recharge_list(request):
   data=[]
   retailers_data=[]
   products_data=[]
   products_id=''
   state_data=get_state()
   recharge_status=''
   count=0
   user_id = request.POST.get('user_id')
   my_user_type=Group.objects.filter(user=user_id).values_list('name','id')
   if my_user_type:
      user_type=my_user_type[0][1]

   if my_user_type:
       q = Q()
       if user_type==2:
           q &= Q(user_id_retailer_id=user_id)
           first_name='user_id_retailer_id__first_name'
           last_name='user_id_retailer_id__last_name'
       if user_type==3:
           q &= Q(user_id_farmer_id=user_id)
           first_name='user_id_farmer_id__first_name'
           last_name='user_id_farmer_id__last_name'

       user_info1=models.Recharge.objects.filter(q).values_list('id',str(first_name),str(last_name),'amount','status','created_at').order_by('-updated_at')
       if user_info1:
           for i in user_info1:
               recharge_id=i[0]
               first_name=i[1]
               last_name=i[2]
               recharge_amount=i[3]
               status=i[4]
               created_at=i[5]
               formatedDate = created_at.strftime("%d-%m-%Y %H:%M:%S")
               if status:
                   status="Complete"
            
               else:
                   status="Pending"
            
               count+=1
               data.append({'recharge_id':recharge_id,'name':str(first_name)+' '+str(last_name),"recharge_amount":str(recharge_amount),'status':str(status),'created_at':formatedDate})
           response=JsonResponse({'status':'success','msg':'All Order List','data':data})
       else:
           response=JsonResponse({'status':'success','msg':'No Order Details Found','data':[]})
   else:
       response=JsonResponse({'status':'success','msg':'No User Details Found','data':[]})

   return response


@csrf_exempt
def get_support_list(request):
    data=[]
    count=0
    user_photo="/media/default/placeholder.png"
    user_info=models.Support.objects.all().values_list('id','query','created_at','user').order_by('-updated_at')
    print(user_info)
    for i in user_info:
        id=i[0]
        query=i[1]
        created_at=i[2]
        user_id=i[3]
        user_info=models.UserProfile.objects.filter(user=user_id).values_list('user__first_name','user__last_name','user_photo')
        for i in user_info:
            first_name=i[0]
            last_name=i[1]
            full_name=str(first_name)+" "+str(last_name)
            user_photo=i[2]
            if user_photo:
                user_photo=user_photo
        
            formatedDate = created_at.strftime("%d/%m/%Y")
            count+=1
            data.append({'count':count,'created_at':formatedDate,'query':query,'support_id':id,'name':full_name,'user_photo':user_photo})
    response=JsonResponse({'status':'success','msg':'Support Details','data':data})
    return response



@csrf_exempt
def reply_support_list(request):
    count=0
    data_reply=[]
    support_id = request.POST.get('support_id')
    user_chats=models.SupportReply.objects.filter(support_id_id=support_id).values_list('id','query','reply','created_at','user_id_admin_id').order_by('created_at')
    for i in user_chats:
        chat_id=i[0]
        chat_query=i[1]
        reply=i[2]
        chat_created_at=i[3]
        chat_formatedDate = chat_created_at.strftime("%d/%m/%Y %H:%M")
        user_id_admin_id=i[4]
        count+=1
        data_reply.append({'count':count,'chat_id':chat_id,'chat_query':chat_query,'reply':reply,'created_at':chat_formatedDate,'user_id_admin_id':user_id_admin_id})

    if request.POST.get('message'):
        reply = request.POST.get('message')
        user_id_admin_id_id = request.user.id
        support = models.SupportReply.objects.create(query=reply,support_id_id=support_id,user_id_admin_id_id=user_id_admin_id_id)
        support.save()
    response=JsonResponse({'status':'success','msg':'Support Details','data':data_reply})
    return response

@csrf_exempt
def send_query_list(request):
    query = request.POST.get('query')
    subject = request.POST.get('subject')
    user_id = request.POST.get('user_id')
    user_id=User.objects.get(id=user_id)
    user_id_admin_id_id = request.POST.get('admin_id')
    support = models.Support.objects.create(subject=subject,user=user_id,query=query)
    support.save()
    support_id=support.id
    support_reply = models.SupportReply.objects.create(query=query,support_id_id=support_id,user_id_admin_id_id=user_id_admin_id_id)
    support_reply.save()
    response=JsonResponse({'status':'success','msg':'Query Send Successfuly','support_id':support_id})
    return response

