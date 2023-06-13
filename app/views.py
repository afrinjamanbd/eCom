from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import  get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import ProductTable
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from app.serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

# Create your views here.
User = get_user_model()

# User HomePage : shows the product list with detail || Allow user to add item in cart
@login_required(login_url='login')
def HomePage(request):
    data = ProductTable.objects.filter(stock_status='available')
    page = Paginator(data,10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page' : page,
        'pagetitle': "Home"
    }
    return render (request,'home.html',context)


# User Profile : user profile 
@login_required(login_url='login')
def Profile(request):
    user = User.objects.get(id=request.user.id)

    # update form for account settings update
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        try:
            user.first_name = fname
            user.last_name = lname
            user.save()
            return render (request,'profile.html',{'username': user.username,'pagetitle': "Profile"})
        except Exception as e:
            return HttpResponse ("OOPS something wrong occured!!!\n" + e)
    context = {'user': user,'pagetitle': "Profile"}
    return render (request,'profile.html',context)


# User Cart : shows selected item by user
@login_required(login_url='login')
def Cart(request):

    # redirect to checkout page for payment
    if request.method=='POST':
        return redirect('checkout')

    # gets selected item's id list from coockies and fetches from database
    selectedItem = list(request.COOKIES.get("selectedItem"))    
    data = ProductTable.objects.filter(id__in=(selectedItem))

    context = {
        'data' : data,
        'pagetitle': "Cart"
    }
    return render (request,'cart.html',context)


# User Checkout : shows order summery and payment option
@login_required(login_url='login')
def Checkout(request):

    # gets selected item's id list from coockies and fetches from database
    selectedItem = list(request.COOKIES.get("selectedItem")) 
    data = ProductTable.objects.filter(id__in=(selectedItem))

    totalItem = len(data)
    totalPrice = 0
    for i in data: totalPrice += i.price
    context = {
        'pagetitle': "Place order",
        'totalItem' : totalItem,
        'totalPrice' : totalPrice,
        'data' : data
        }
    return render (request,'orderpage.html',context)


# API ProductApi : Third Party Product detail and purchase
@login_required(login_url='loginapi')
@csrf_exempt
def ProductApi(request):
    
    # returns json data for all the products 
    if request.method == 'GET':
        product = ProductTable.objects.all()
        productsSerializer = ProductSerializer(product,many=True)
        return JsonResponse(productsSerializer.data,safe=False)

    # gets json data from request body for selected products 
    elif request.method == 'POST':
        productData = JSONParser().parse(request)
        productsSerializer = ProductSerializer(data = productData)

        if productsSerializer.is_valid():
            try:
                # makes payment 
                result = gateway.transaction.sale({
                    "amount" : request.form["amount"],
                    "payment_method_nonce" : request.form["payment_method_nonce"],
                    "device_data": request.form["device_data"],
                    "order_id" : "Mapped to PayPal Invoice Number",
                    "options" : {
                        "submit_for_settlement": True,
                        "paypal": {
                            "custom_field" : "PayPal custom field",
                            "description" : "Description for PayPal email receipt",
                    },
                    },
                })
                if result.is_success:
                    "Success ID: ".format(result.transaction.id)
                    ## update stock
                    return JsonResponse('Thanks for shopping',safe = False)
                else:
                    format(result.message)
                    return JsonResponse('Error Occured during payment ' ,safe = False)
            except Exception as e:
                return JsonResponse('Error Occured : ' + e,safe = False)

        return JsonResponse('Request Failed',safe = False)
     

# API LoginApi : Third Party Login 
@csrf_exempt
def LoginApi(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return JsonResponse('Logged in',safe = False)
        else:
            return JsonResponse('Request Failed',safe = False)
    return JsonResponse('Please Log in First',safe = False)


# API LogoutApi : Third Party Logout 
def LogoutApi(request):
    logout(request)
    return JsonResponse('Logged out',safe = False)


# User Signup : User SIgnup
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html',{'pagetitle': "Register"})


# User LoginPage : User Login 
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'login.html',{'pagetitle': "eCommerce App"})


# User LogoutPage : User Logout
def LogoutPage(request):
    logout(request)
    return redirect('login')