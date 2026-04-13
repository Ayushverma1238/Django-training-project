from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def product(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        type = request.POST.get('type')

        Product.objects.create(
            image=image,
            title=title,
            price=price,
            discount=discount,
            desc=desc,
            category=category,
            type=type
        )

    data = Product.objects.all()
    return render(request, 'product.html', {'data': data})

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

# def addProduct(request):
#     if request.method == 'POST':
#         image = request.POST.get('imageUrl')
#         title = request.POST.get("name")
#         desc = request.POST.get("email")
#         price = request.POST.get("phoneNo")
#         category = request.POST.get("message")
#         type = request.POST.get("message")
#         discount = request.POST.get("message")
#         c = Contact(image = image, title = title, desc = desc, price = price, discount = discount, category = category, type = type)
#         c.save()
#         return redirect('/product')

def signupView(request):
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if(password != cpassword):
            return 
        
        user = User.objects.create_user(userName, email, password)
        user.first_name =  firstName
        user.last_name = lastName
        user.save()
        return redirect('/login')

    return render(request, 'signup.html')

@ensure_csrf_cookie
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
            return render(request, 'login.html', {"error":'Username or Password is incorrect'})

    return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return render(request, 'index.html')

