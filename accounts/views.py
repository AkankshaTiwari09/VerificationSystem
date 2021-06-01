from django.shortcuts import render, redirect
from django.contrib.auth.models import User              # for creating user
from django.contrib import messages                      # for message popups
from django.conf import settings                         # for settings in mail function
from django.core.mail import send_mail    
from django.contrib.auth import authenticate,login,logout               #for sending mail
from django.contrib.auth.decorators import login_required
from .models import *
import uuid

# Create your views here.


@login_required(login_url="login")
def home(request):
    return render(request,'home.html')

def logout_request(request):
    logout(request)
    messages.success(request,"You have successfully logged out.")
    return redirect("login")

def login_attempt(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(email=email).first()
        if email == "" or password == "":
            messages.error(request,"Please fill all the fields")
            return redirect("login")
        
        if user_obj is None:
            messages.error(request,"User does not exist.")
            return redirect("login")

        username=user_obj.get_username()
        #print(username)
        user_profile= Profile.objects.filter(user=user_obj).first()
        if not user_profile.is_verified:
            messages.error(request,"Please verify your account before logging in. Check you mailbox for verification mail.")
            return redirect("login")

        user=authenticate(username=username,password=password)        # By default authentication can be done with username and password only
        if user is None:
            messages.error(request,"Wrong email id or password")
            return redirect("login")
        
        else:
            login(request,user)
            return redirect("/")
        
    return render(request,"login.html")

def register_attempt(request):

    if request.method=='POST':
        username=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        #print(username,email)

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is already taken')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                print(User.objects.filter(email=email).first())
                messages.error(request, 'Email is already taken')
                return redirect('/register')

            user_obj=User.objects.create(username=username,email=email)    # user_obj is the name of the object that we are creating. The name can be anything
            user_obj.set_password(password)
            user_obj.save()  
            
            auth_token=str(uuid.uuid4())
            profile_obj= Profile.objects.create(user=user_obj, auth_token=auth_token)  # profile_obj is the name of the profile class object
            #uuid is being used for token. import uuid before use. uuid needs to be converted to string.
            profile_obj.save()
            send_mail_after_registration(username,email,auth_token)

            return redirect('/token')

        except Exception as e:
            print(e)

    #messages.success(request, 'Profile created')
    return render(request,"register.html")

def success(request):
    return render(request,"success.html")

def token_send(request):
    return render(request,"token_send.html")

def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,"Your account is already verified")
                return redirect("login")
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request,"Your account has been verified")
            return redirect("login")
        else:
            return redirect("error")
    except exception as e:
        print(e)

def error_page(request):
    return render(request,"error.html")


def send_mail_after_registration(username,email,token):
    subject="Account Verification for django"
    message= f"Hi {username},\nPlease click on the below link for account verification.\n\n http://127.0.0.1:8000/verify/{token}"   # string formatting
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)