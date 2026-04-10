from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def about(request):
    return render(request,"login.html")

def about(request):
    return render(request,"signUp.html")


def product(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "product.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phoneNo = request.POST.get("phoneNo")
        message = request.POST.get("message")
        c = Contact(name = name, email = email, phoneNo = phoneNo, message = message)
        c.save()
        return redirect('/contact')
    data = Contact.objects.all()


    return render(request,"contact.html", {'data' :data})

def signupView(request):

    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        user = User.objects.create_user(userName, email, password)
        user.first_name =  firstName
        user.last_name = lastName
        user.save()
        return redirect('/login')

    return render(request, 'signup.html')

def loginView(request):
    if request.method == "POST":
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        user = authenticate(request, username=userName, password=password)

        if user is not None:
            # 2. Start the session
            login(request, user)
            return redirect('/') 
        else:
            # 3. Handle failed login
            # messages.error(request, "Invalid username or password")
            return render(request, 'login.html')

    return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return render(request, 'index.html')