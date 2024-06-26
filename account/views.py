from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"User already exist")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email aready exist")
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,password=password1,email=email,username=username)
                user.save()
                print("Succesfull")
                return redirect('login')
            
        else:
            messages.info(request,"password is not matching")
            return redirect('register')
    else:
        return render(request,'register.html')
    
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')