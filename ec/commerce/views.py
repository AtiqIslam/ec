from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Order


PRODUCTS = [
    {
        "id": "panjabi-1",
        "name": "Premium Cotton Panjabi",
        "price": 1500,
        "old_price": 2000,
        "discount": "25%",
        "rating": "4.8",
        "image": "images/panjabi1.jpg",
    },
    {
        "id": "panjabi-2",
        "name": "Classic Eid Panjabi",
        "price": 1700,
        "old_price": 2200,
        "discount": "25%",
        "rating": "4.8",
        "image": "images/panjabi2.jpg",
    },
    {
        "id": "panjabi-3",
        "name": "Embroidered Panjabi",
        "price": 1750,
        "old_price": 2300,
        "discount": "24%",
        "rating": "4.9",
        "image": "images/panjabi3.webp",
    },
    {
        "id": "panjabi-4",
        "name": "Festive White Panjabi",
        "price": 1650,
        "old_price": 2100,
        "discount": "21%",
        "rating": "4.7",
        "image": "images/panjabi4.jpg",
    },
    {
        "id": "panjabi-5",
        "name": "Royal Blue Panjabi",
        "price": 1800,
        "old_price": 2400,
        "discount": "25%",
        "rating": "4.8",
        "image": "images/panjabi5.jpg",
    },
    {
        "id": "panjabi-6",
        "name": "Modern Fit Panjabi",
        "price": 1725,
        "old_price": 2250,
        "discount": "23%",
        "rating": "4.6",
        "image": "images/panjabi6.jpg",
    },
    {
        "id": "panjabi-7",
        "name": "Elegant Black Panjabi",
        "price": 1850,
        "old_price": 2450,
        "discount": "24%",
        "rating": "4.9",
        "image": "images/panjabi7.jpg",
    },
    {
        "id": "panjabi-8",
        "name": "Signature Collection Panjabi",
        "price": 1900,
        "old_price": 2500,
        "discount": "24%",
        "rating": "4.9",
        "image": "images/panjabi-9.jpg",
    },
]

PRODUCT_LOOKUP = {product["id"]: product for product in PRODUCTS}


def get_cart(request):
    return request.session.get("cart", {})


def get_cart_count(request):
    return sum(get_cart(request).values())


def build_cart_items(request):
    cart = get_cart(request)
    items = []

    for product_id, quantity in cart.items():
        product = PRODUCT_LOOKUP.get(product_id)
        if not product:
            continue

        item = product.copy()
        item["quantity"] = quantity
        item["subtotal"] = product["price"] * quantity
        items.append(item)

    return items


def base_context(request):
    return {"cart_count": get_cart_count(request)}


def build_checkout_context(request, cart_items, form_data=None, errors=None):
    total = sum(item["subtotal"] for item in cart_items)
    return {
        **base_context(request),
        "cart_items": cart_items,
        "cart_total": total,
        "form_data": form_data or {},
        "form_errors": errors or {},
    }


def home(request):
    context = {
        **base_context(request),
        "products": PRODUCTS,
    }
    return render(request, "home.html", context)

def login_form(request):
    if request.method == 'POST':
        frm=AuthenticationForm(request, data=request.POST)
        if frm.is_valid():
            username=frm.cleaned_data['username']
            password=frm.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("success")
    else:
        frm = AuthenticationForm()
    return render(request, 'login.html', {'form':frm, **base_context(request)})

def cart_view(request):
    cart_items = build_cart_items(request)
    total = sum(item["subtotal"] for item in cart_items)
    context = {
        **base_context(request),
        "cart_items": cart_items,
        "cart_total": total,
    }
    return render(request, "cart.html", context)


def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")

    if product_id not in PRODUCT_LOOKUP:
        return redirect("home")

    cart = get_cart(request)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session["cart"] = cart
    request.session.modified = True

    next_url = request.POST.get("next") or "home"
    return redirect(next_url)


def checkout_view(request):
    cart_items = build_cart_items(request)
    if not cart_items:
        return redirect("cart")

    context = build_checkout_context(request, cart_items)
    return render(request, "checkout.html", context)


def confirm_order(request):
    if request.method != "POST":
        return redirect("checkout")

    cart_items = build_cart_items(request)
    if not cart_items:
        return redirect("cart")

    form_data = {
        "customer_name": request.POST.get("customer_name", "").strip(),
        "phone_number": request.POST.get("phone_number", "").strip(),
        "district": request.POST.get("district", "").strip(),
        "thana": request.POST.get("thana", "").strip(),
        "address": request.POST.get("address", "").strip(),
    }
    errors = {}

    for field, value in form_data.items():
        if not value:
            errors[field] = "This field is required."

    if errors:
        context = build_checkout_context(request, cart_items, form_data=form_data, errors=errors)
        return render(request, "checkout.html", context)

    total = sum(item["subtotal"] for item in cart_items)
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        customer_name=form_data["customer_name"],
        phone_number=form_data["phone_number"],
        district=form_data["district"],
        thana=form_data["thana"],
        address=form_data["address"],
        items=[
            {
                "product_id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "subtotal": item["subtotal"],
            }
            for item in cart_items
        ],
        total_price=total,
    )

    request.session["cart"] = {}
    request.session.modified = True

    context = {
        "cart_count": 0,
        "title": "Order Confirmed",
        "message": "Your order has been confirmed successfully.",
        "details": f"{len(cart_items)} item(s) confirmed. Total: Tk {total}",
        "order_number": order.order_number,
        "customer_name": order.customer_name,
        "phone_number": order.phone_number,
        "district": order.district,
        "thana": order.thana,
        "address": order.address,
        "button_url": "home",
        "button_text": "Continue Shopping",
    }
    return render(request, "success.html", context)
  
def form_view(request):
    if request.method == 'POST':
      frm =UserCreationForm(request.POST)
      if frm.is_valid():
        frm.save()
        return redirect("success")
    else:
        frm = UserCreationForm()
    return render(request, 'form.html', {'form':frm, **base_context(request)}) 

def success(request):
    context = {
        **base_context(request),
        "title": "Success",
        "message": "Your action has been completed successfully.",
        "details": "Thank you for using MyShop.",
        "button_url": "home",
        "button_text": "Back to Home",
    }
    return render(request, 'success.html', context)
    
