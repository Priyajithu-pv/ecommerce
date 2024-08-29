from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
import uuid

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
     #checking both the passwords entered is same or not
        if password1 == password2:
            #checking whether entered username is already exists or not,
            if User.objects.filter(username=username).exists():
                messages.info(request,'username is already taken')
                return redirect('register')
            # checking whether entered emailid is already exists or not,
            elif User.objects.filter(email=email).exists():
                messages.info(requset,'email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
        else:
            messages.info(request,"password not correct")
            return redirect('register')

        return redirect('login')
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            uid= str(uuid.uuid4())            #generate a random UID
            request.session['uid'] = uid      #Add the UID to the session
            request.session['username'] = username    #Adding username to session
            return redirect('/')                       #return to home page
        else:
            messages.info(request,'invalid details')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')