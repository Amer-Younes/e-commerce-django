from django.shortcuts import render , redirect , get_object_or_404
from core.models import CartOrder , Product , Category , CartOrderItem , ProductReview 
from django.db.models import Sum
from userauths.models import User , Profile
import datetime
from .forms import AddProductForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
# Create your views here.



@admin_required
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum('price'))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by('-id')
    latest_orders = CartOrder.objects.all()


    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum('price'))
    if monthly_revenue['price'] is None:
        monthly_revenue['price'] = 0

    context = {
        'revenue': revenue,
        'total_orders_count': total_orders_count,
        'all_products': all_products,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'latest_orders': latest_orders,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'useradmin/dashboard.html', context)


@admin_required
def products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    context = {
        'all_products': all_products,
        'all_categories': all_categories,
    }
    return render(request, 'useradmin/products.html', context)

@admin_required
def addProductView(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:dashboard')
    else:
        form = AddProductForm()
    
    context ={
        'form': form,
        }

    return render(request, 'useradmin/add_product.html' , context )



@admin_required
def editProductView(request , pid):
    product = Product.objects.get(pid=pid)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES , instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:edit-product' , product.pid)
    else:
        form = AddProductForm(instance=product)
    context ={
        'form': form,
        'product': product,
        }
    return render(request, 'useradmin/edit_product.html' , context )
    

@admin_required
def deleteProductView(request , pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect('useradmin:products')


@admin_required
def orders(request):
    orders = CartOrder.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'useradmin/orders.html', context)

@admin_required
def orderDetails(request , id):
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'useradmin/order-details.html', context)



@admin_required
def updateOrderStatus(request, id):
    if request.method == 'POST':
        order = get_object_or_404(CartOrder, id=id)
        new_status = request.POST.get('status')
        # Update correct field name (product_status instead of status)
        order.product_status = new_status
        order.save()
        return redirect('useradmin:order-detail', id=order.id)


@admin_required
def shopPage(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum('price'))
    total_sales = CartOrderItem.objects.filter(order__paid_status=True).aggregate(qty=Sum('qty'))

    context = {
        'products': products,
        'revenue': revenue,
        'total_sales': total_sales,
    }
    return render(request, 'useradmin/shop-page.html', context)

@admin_required
def reviews(request):
    reviews = ProductReview.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, 'useradmin/reviews.html' , context)



@admin_required
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        image = request.FILES.get('image')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        country = request.POST.get('country')
        if image is not None:
            profile.image = image
        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        profile.address = address
        profile.country = country
        profile.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('useradmin:settings')

    context = {
        'profile': profile,
    }
    return render(request, 'useradmin/settings.html' , context)


@admin_required
def changePassword(request):
    user = request.user
    if request.method =="POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")
        if confirm_password != new_password:
            messages.warning(request, "Password does not match")
            return redirect('useradmin:change-password')
        if check_password(old_password , user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('useradmin:change-password')
        else:
            messages.warning(request, "Old Password Is Incorrect")
            return redirect('useradmin:change-password')
    
    return render(request , "useradmin/change-password.html")

