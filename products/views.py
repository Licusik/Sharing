from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from products.forms.create import CreateProduct
from products.forms.edit import EditProduct
from products.forms.forms import BookingForm
from products.forms.product_form import ProductForm
from products.models import Product, Booking, Favorite
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    products = Product.objects.all().order_by("id")
    return render(request, "index.html", {"products": products})


def catalog(request):
    category = request.GET.get("category")
    products = Product.objects.all()
    if category and category != "all":
        products = products.filter(category=category)

    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("size", 5)
    page = Paginator(products, page_size).get_page(page_number)

    return render(request, "catalog.html", {
        "products": page.object_list,
        "total_count": products.count(),
        "page": page,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(product=product, user=request.user).exists()

    return render(request, "product_detail.html", {
        "product": product,
        "is_favorite": is_favorite,
    })



def product_create(request):
    form = CreateProduct(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Продукт створено!")
        return redirect("admin_panel")
    return render(request, "create.html", {"form": form})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = EditProduct(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST":
        if request.FILES and product.image:
            product.image.delete(save=False)
        if form.is_valid():
            form.save()
            messages.success(request, "Продукт оновлено!")
            return redirect("admin_panel")
    return render(request, "edit.html", {"form": form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.image:
        product.image.delete(save=False)
    product.delete()
    messages.success(request, "Продукт видалено!")
    return redirect("admin_panel")


def book_car(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.product = product
            overlap = Booking.objects.filter(
                product=product,
                date_from__lt=booking.date_to,
                date_to__gt=booking.date_from
            ).exists()
            if overlap:
                messages.error(request, "Ці дати вже зайняті.")
            elif product.stock <= 0:
                messages.error(request, "Автомобіль недоступний.")
            else:
                product.stock -= 1
                product.save()
                booking.save()
                messages.success(request, "Бронювання успішне!")
                return redirect("/")
    else:
        form = BookingForm(initial={"product": product})
    return render(request, "booking.html", {"form": form, "product": product})


def booking_dates(request, product_id):
    bookings = Booking.objects.filter(product_id=product_id)
    return render(request, "booking_dates.html", {"bookings": bookings})


def booked_dates(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bookings = Booking.objects.filter(product=product)
    return render(request, "booked_dates.html", {"product": product, "bookings": bookings})


def admin_panel(request):
    products = Product.objects.all()
    bookings = Booking.objects.select_related("product").all()

    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Продукт додано!")
        return redirect("admin_panel")

    return render(request, "admin_panel.html", {
        "products": products,
        "form": form,
        "bookings": bookings
    })


def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Бронювання оновлено!")
        return redirect("admin_panel")
    return render(request, "admin_panel.html", {
        "products": Product.objects.all(),
        "bookings": Booking.objects.all(),
        "form": form,
    })


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    messages.success(request, "Бронювання видалено!")
    return redirect("admin_panel")

def set_cookie(request):

    response = HttpResponse("Cookie Set")
    response.set_cookie('favorite_product', 'product_id')  
    return response

def get_cookie(request):

    favorite_product = request.COOKIES.get('favorite_product')
    return HttpResponse(f"Favorite Product ID: {favorite_product}")


def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite_products = request.session.get('favorite_products', [])

    if product.id in favorite_products:
        favorite_products.remove(product.id)  
        messages.info(request, "Товар видалено з обраного")
    else:
        favorite_products.append(product.id) 
        messages.success(request, "Товар додано до обраного")

    request.session['favorite_products'] = favorite_products  

    return redirect(request.META.get('HTTP_REFERER', '/'))



def favorite_list(request):

    favorite_products = request.session.get('favorite_products', [])


    products = Product.objects.filter(id__in=favorite_products)
    
    return render(request, 'favorite_list.html', {'products': products})
