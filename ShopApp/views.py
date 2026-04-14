from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, Product, Wishlist, Cart, CartItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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

        
        if not Product.objects.filter(title=title).exists():
            Product.objects.create(
                image=image,
                title=title,
                price=price,
                discount=discount,
                desc=desc,
                category=category,
                type=type
            )

        return redirect('product')

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


# WishList item details
def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {'wishlist_items': items})

def add_to_wishlist(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    product = Product.objects.get(id=id)

    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        Wishlist.objects.create(user=request.user, product=product)

    return JsonResponse({"status": "added"})


def remove_from_wishlist(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        wishlist_item = Wishlist.objects.get(id=id, user=request.user)
        wishlist_item.delete()
    except Wishlist.DoesNotExist:
        pass

    return JsonResponse({"status": "deleted"})


def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)

    product = Product.objects.get(id=id)

    # ✅ ALWAYS use get_or_create
    cart, created = Cart.objects.get_or_create(user=request.user)

    # ✅ Check if item already exists
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({'status': 'added'})
# cart item
def cart(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    items = Cart.objects.filter(user=request.user)

    return render(request, 'bag.html', {'cart_items': items})


# Women, Man, Kids collection

def women(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    data = Product.objects.filter(category = "women")
    return render(request, 'women.html', {'data': data})


def men(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    data = Product.objects.filter(category = "men")
    return render(request, 'mens.html', {'data': data})


def kids(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    data = Product.objects.filter(category = "kids")
    return render(request, 'kids.html', {'data': data})

def remove_from_cart(request, id):
    print("ID RECEIVED:", id)

    try:
        item = CartItem.objects.get(id=id)
        print("FOUND ITEM:", item)

        item.delete()
        return JsonResponse({"status": "removed"})

    except CartItem.DoesNotExist:
        print("NOT FOUND ❌")
        return JsonResponse({"error": "Item not found"}, status=404)

from django.shortcuts import render
from .models import Cart, CartItem

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    # ✅ Get or create cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # ✅ Get items
    cart_items = CartItem.objects.filter(cart=cart)

    # ✅ Calculate total
    total_mrp = sum(i.product.price * i.quantity for i in cart_items)
    delivery = 50 if total_mrp > 0 else 0
    total = total_mrp + delivery

    context = {
        "cart_items": cart_items,
        "total_mrp": total_mrp,
        "delivery": delivery,
        "total": total
    }

    return render(request, "bag.html", context)

def update_cart_qty(request):
    item_id = request.GET.get('id')
    qty = int(request.GET.get('qty'))

    item = Cart.objects.get(id=item_id)
    item.quantity = qty
    item.save()

    # Recalculate cart
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_mrp = sum(i.product.price * i.quantity for i in cart_items)
    discount = sum((i.product.old_price - i.product.price) * i.quantity for i in cart_items)
    
    delivery = "FREE" if total_mrp > 500 else 50
    total = total_mrp - discount + (0 if delivery == "FREE" else delivery)

    item_total = item.product.price * item.quantity
    print(cart_items, total_mrp)
    return JsonResponse({
        'total_mrp': total_mrp,
        'discount': discount,
        'delivery': delivery,
        'total': total,
        'item_total': item_total   # 👈 new
    })