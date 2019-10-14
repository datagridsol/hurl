# dappx/views.py
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
    registered = False
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
def addUser(request):
    gr_no=[]
    user_type=Group.objects.all().values_list('id', 'name')
    for i in user_type:
        gr_no.append(i[1])

    print(request.user.id)
    my_user_type=Group.objects.filter(user=request.user.id).values_list('name')
    print(my_user_type[0][0])
    if request.method == 'POST':
        data={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        user_type = request.POST.get('user_type')
        print("values",user_type)
        new_user = User.objects.create(username = username,password = password)
        new_user.set_password(password)
        new_user.save()
        new_Uid = new_user.id
        print("new_Uid",new_Uid)
        userprofile = models.UserProfile.objects.create(user_id=new_Uid,user_type="re",address=address)
        userprofile.save()
        #new_user.set_password(password)
        #new_user = User.objects.create(username=username,password=password)
        #new_user = form.save(commit=False)
        #new_user.save()
        #user = User.objects.create(username=username,password=password)
        #user.save()
        #new_id=new_user.id
        #userprofile = models.UserProfile.objects.create(user=new_id,user_type="re",address=address)
        #userprofile.save()
        #remember_me = request.POST.get('remember_me')
        #print("Insideeee",remember_me)
        data={'user_type':user_type,'address':address,"status":True}
        return render(request, 'manage_user.html', {'data':data})

    else:
        print("Get Method",gr_no)
        return render(request, 'userprofile.html', {'data':gr_no})


@csrf_exempt
def get_manage_user(request):
    data=[]
    user_type=""
    district=""
    state=""
    userdata=User.objects.all().values_list('id', 'first_name','last_name','username','is_active')
    for nlist in userdata:
        row=[]
        user_id=nlist[0]
        first_name=nlist[1]
        last_name=nlist[2]
        full_name=str(first_name)+" "+str(last_name)
        username=nlist[3]
        status=nlist[4]
        if status:
            status="Active"
        else:
            status="Deactive"

        user_info=models.UserProfile.objects.filter(user=user_id).values_list('user_type__name','district__district_name','state__state_name')
        for i in user_info:
            user_type=i[0]
            district=i[1]
            state=i[2]

        row.append(user_id)
        row.append(user_type)
        row.append(full_name)
        row.append(username)
        row.append(district)
        row.append(state)
        row.append(status)
        data.append(row)
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
