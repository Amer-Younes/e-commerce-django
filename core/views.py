from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product , Coupon , Category , Vendor , CartOrder , CartOrderItem , ProductImages , Wishlists , Address , ProductReview 
from userauths.models import ContactUs , Profile
from django.db.models import Count , Avg
from taggit.models import Tag
from .forms import ProductReviewForm
from django.http import  JsonResponse
from django.template.loader import render_to_string
from django.db.models import Min, Max
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
import calendar
import stripe




# Create your views here.



def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published" , featured=True)
    

    context = {
        "products" : products,
        
    }
    return render(request , 'core/index.html' , context)



def productListView(request):
    products= Product.objects.filter(product_status="published" )
    
    context = {
        "products" : products
    }
    return render(request , 'core/product-list.html' , context)



def categoryListView(request):
    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(product_count=Count("product"))
    context = {
        "categories" : categories
    }
    return render(request , 'core/category-list.html' , context)



def categoryProductListView(request , cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status = "published" , category = category)

    context={
        "category" : category ,
        "products" : products ,
    }
    return render(request , "core/category-product-list.html" ,context)



def vendorListView(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors" : vendors,
    }
    return render(request , "core/vendor-list.html" , context)



def vendorDetailView(request , vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status = "published" , vendor=vendor)
    context = {
        "vendor" : vendor,
        "products" : products,
    }
    return render(request , "core/vendor-detail.html" , context)



def productDetailView(request , pid):
    product = Product.objects.get( pid=pid)
    # product = get_object_or_404(Product , pid=pid)
    products = Product.objects.filter(category = product.category , product_status = "published").exclude(pid=pid)[:4]

    # Getting All Reviews Related To Product

    reviews = ProductReview.objects.filter(product=product).order_by("-id")

    # Getting Average Review
    average_rating = ProductReview.objects.filter(product=product ).aggregate(rating=Avg('rating'))


    # Product Review Form
    review_form = ProductReviewForm

    make_review = True

    if request.user.is_authenticated:
        uesr_review_count = ProductReview.objects.filter(user=request.user , product=product).count()
        if uesr_review_count >0 :
            make_review = False



    product_images = product.product_images.all()
    
    context = {
        "product" : product , 
        "product_images" : product_images , 
        "products" : products , 
        "reviews" : reviews , 
        "average_rating" : average_rating , 
        "review_form" : review_form , 
        "make_review" : make_review , 
    }
    return render(request , "core/product-detail.html"  ,context )



def tagList(request , tag_slug=None):
    products = Product.objects.filter( product_status = "published").order_by("-id")
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag , slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products":products,
        "tag":tag,

    }
    return render(request , "core/tag.html" , context)



def ajaxAddReview(request , pid):
    
    product = Product.objects.get(pid = pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user ,
        product = product ,
        review = request.POST['review' ],
        rating = request.POST['rating'],
    )
    context ={
        'user' :user.username ,
        'review' :request.POST['review' ] ,
        'rating' :request.POST['rating'] ,
    }
    average_rating = ProductReview.objects.filter(product=product ).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool' : True ,
        'context' : context ,
        'average_rating' : average_rating ,
        }
    )



def searchView(request):
    query = request.GET.get("q")
    products = Product.objects.filter(title__icontains = query ).order_by("-date")

    context = {

        "products": products ,
        "query":query ,
    }

    return render(request , "core/search.html"  ,context )



def filterProductView(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET["min_price"]
    max_price = request.GET["max_price"]

    products = Product.objects.filter(product_status="published" ).order_by("-id").distinct()

    products = products.filter(price__gte = min_price) # gte mean greater than or equal to
    products = products.filter(price__lte = max_price) # lte mean less than or equal to



    if (len(categories) >0 ):
        products = products.filter(category__id__in=categories).distinct()

    if (len(vendors) >0 ):
        products = products.filter(vendor__id__in=vendors).distinct()

    context = {
        "products":products,
    }
    product_count = products.count()

    data = render_to_string("core/async/product-list.html" , context)

    return JsonResponse({
        "data":data ,
        "product_count":product_count ,
        

    })



@login_required
def addToCartView(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] ={ 
        'title' : request.GET['title'] ,
        'qty' : request.GET['qty'] ,
        'price' : request.GET['price'] ,
        'image' : request.GET['image'] ,
        'pid' : request.GET['pid'] ,
    }

    if 'cart_data_obj' in request.session :
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[request.GET['id']]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else :
            cart_data= request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else :
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({
        'data' : request.session['cart_data_obj'] ,
        'totalCartItems' : len(request.session['cart_data_obj'])
    })



def cartView(request):
    cart_total_amount =0
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
        context = {
        'cart_data' : request.session['cart_data_obj'] ,
        'totalCartItems' : len(request.session['cart_data_obj']) ,
        'cart_total_amount':cart_total_amount
    }
        return render(request , "core/cart.html" , context)
    
    else:
        context = {
        'cart_data' : '' ,
        'totalCartItems' : 0 ,
        'cart_total_amount':cart_total_amount
    }
        messages.warning(request , "Your Cart Is Empty")
        return render(request , "core/cart.html" , context)



def deleteFromCartView(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session :
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount =0
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        

    context = render_to_string("core/async/cart-list.html" , {
        'cart_data' : request.session['cart_data_obj'] ,
        'totalCartItems' : len(request.session['cart_data_obj']) ,
        'cart_total_amount':cart_total_amount
    })
    return JsonResponse({
        "data" : context ,
        'totalCartItems' : len(request.session['cart_data_obj']) ,
    })

def updateProductFromCartView(request):
    product_id = str(request.GET['id'])
    product_qty = int(request.GET['qty'])
    if 'cart_data_obj' in request.session :
        if product_id in request.session['cart_data_obj']:
            request.session['cart_data_obj'][product_id]['qty'] = product_qty
            request.session.modified = True

    cart_total_amount =0
    if 'cart_data_obj' in request.session:
        for product_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        

    context = render_to_string("core/async/cart-list.html" , {
        'cart_data' : request.session['cart_data_obj'] ,
        'totalCartItems' : len(request.session['cart_data_obj']) ,
        'cart_total_amount':cart_total_amount
    })
    return JsonResponse({
        "data" : context ,
        'totalCartItems' : len(request.session['cart_data_obj']) ,
    })



# @login_required
# def checkoutView(request):
#     cart_data = request.session.get("cart_data_obj", {})
    
#     if not cart_data:  # Redirect if cart is empty
#         return redirect("core:cart")

#     cart_total_amount = sum(int(item["qty"]) * float(item["price"]) for item in cart_data.values())

#     # Create Order
#     order = CartOrder.objects.create(user=request.user, price=cart_total_amount)

#     # Add Items to Order
#     for item in cart_data.values():
#         CartOrderItem.objects.create(
#             order=order,
#             invoice_no=f"INVOICE_NO-{order.id}",
#             item=item["title"],
#             image=item["image"],
#             qty=item["qty"],
#             price=item["price"],
#             total=int(item["qty"]) * float(item["price"]),
#         )

#     # PayPal Payment Configuration
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': cart_total_amount,
#         'item_name': f"order-Item-No-{order.id}",
#         'invoice': f"INVOICE_NO-{order.id}",
#         'currency_code': "USD",
#         'notify_url': request.build_absolute_uri(reverse("core:paypal-ipn")),
#         'return_url': request.build_absolute_uri(reverse("core:payment-completed")),
#         'cancel_url': request.build_absolute_uri(reverse("core:payment-failed")),
#     }
    
#     paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

#     try:
#         active_address = Address.objects.get(user=request.user , status=True)
#     except:
#         messages.warning(request , "There are multiple address , only one should be activated ")
#         active_address = None


#     context = {
#         "cart_data": cart_data,
#         "totalCartItems": len(cart_data),
#         "cart_total_amount": cart_total_amount,
#         "paypal_payment_button": paypal_payment_button,
#         "active_address": active_address,
#     }
    
#     return render(request, "core/checkout.html", context)


def checkoutView(request , oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItem.objects.filter(order=order)

    if request.method == "POST":
        code = request.POST.get("code")
        coupon = Coupon.objects.filter(code=code , active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request , "Coupon Already Applied")
                return redirect("core:checkout" , order.oid)
            else:
                discount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                order.price -= discount
                order.saved +=discount
                order.save()

                messages.success(request , "Coupon Activated")
                return redirect("core:checkout" , order.oid)
                
        else:
            messages.warning(request , "Invalid Coupon")
            return redirect("core:checkout" , order.oid)



    context = {
        "order":order,
        "order_items":order_items,
        "strip_publishable_key":settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , "core/checkout.html" , context)

@csrf_exempt
def createCheckoutSession(request , oid):
    order= CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types=['card'],
        line_items=[
            {
                "price_data": {
                    'currency': 'USD',
                    'product_data': {
                        'name': order.full_name
                    },
                    'unit_amount': int(order.price * 1000),
                },
                "quantity": 1
            },
        ] ,
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse("core:payment-completed" , args=[order.oid])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse("core:payment-failed")),
    )

    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    return JsonResponse({
        "sessionId":checkout_session.id,
    })








def saveCheckoutInfo(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("shipping_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['address'] = address
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country


        if "cart_data_obj" in request.session:
            for product_id , item in request.session["cart_data_obj"].items():
                total_amount+= int(item['qty'])*float(item['price'])

            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                full_name=full_name,
                email=email,
                phone=mobile,
                address=address,
                city=city,
                state=state,
                country=country,
            )

            del request.session['full_name']
            del request.session['email']
            del request.session['mobile']
            del request.session['address']
            del request.session['city']
            del request.session['state']
            del request.session['country']

            
            for product_id , item in request.session["cart_data_obj"].items():
                cart_total_amount+= int(item['qty'])*float(item['price'])

                cart_order_item = CartOrderItem.objects.create(
                    order=order,
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=int(item['qty'])*float(item['price']),
                    invoice_no=f"INVOICE_NO-{order.id}",
                )

        return redirect("core:checkout" , order.oid)
    return redirect("core:checkout" , order.oid)


@login_required
def paymentCompleteView(request , oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    context = {
        "order":order,
    }
    
    return render(request ,"core/payment-complete.html" , context )



@login_required
def paymentFailedView(request):
    return render (request ,"core/payment-failed.html" )



@login_required
def customerDashboardView(request):
    order_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    profile = Profile.objects.get(user=request.user)


    orders = CartOrder.objects.annotate(month= ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month" , "count")
    month = []
    total_orders = []
    for order in orders :
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])



    if request.method == "POST" :
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        new_address = Address.objects.create(
            user=request.user ,
            address=address ,
            phone = phone
        )
        messages.success(request , "Added Address Successfully")
        return redirect("core:dashboard")

    context = {
        "profile":profile , 
        "order_list":order_list , 
        "orders":orders , 
        "addresses":address , 
        "months":month , 
        "total_orders":total_orders , 
    }
    return render (request ,"core/dashboard.html"  , context)



def order_detail(request , id):
    order = CartOrder.objects.get(user=request.user , id=id)
    products = CartOrderItem.objects.filter(order=order)
    context ={
        
        "products": products ,
    }
    return render(request , "core/order-detail.html" , context)



def defaultAddress(request):
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)

    return JsonResponse({
        "boolean" : True ,
        
    })



def wishlistPageView(request):
    try:
        wishlist = Wishlists.objects.filter(user=request.user)
    except:
        wishlist = None
    context = {
        "wishlists":wishlist , 
    }
    return render(request , "core/wishlist.html" , context)



@login_required
def deleteFromWishlistView(request):
    product_id = request.GET['id']

    product = Product.objects.get(id = product_id)
    
    wishlist_item = Wishlists.objects.filter(product=product).delete()

    wishlist_count = Wishlists.objects.filter(user=request.user).count()
    
    wishlist = Wishlists.objects.filter(user=request.user)
    
    
    context = render_to_string("core/async/wishlist-list.html" , {
        "wishlist_count":wishlist_count,
        "wishlist":wishlist,
    })
    return JsonResponse({
        "data":context,
        "wishlist_count":wishlist_count,
    })



@login_required
def toggleWishlist(request):
    id = request.GET.get('id')
    product = Product.objects.get(id=id)
    wishlist_item, created = Wishlists.objects.get_or_create(user=request.user, product=product)
    
    if created:
        action = "added"
    else:
        wishlist_item.delete()
        action = "removed"
    
    wishlist_count = Wishlists.objects.filter(user=request.user).count()

    return JsonResponse({"status": "success",
                        "action": action,
                        "wishlist_count": wishlist_count,
                        })



def contactView(request):
    return render(request , "core/contact.html")

def ajaxContactView(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    message = request.GET['message']
    subject = request.GET['subject']
    phone = request.GET['phone']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        message=message,
        subject=subject,
        phone=phone,
    )

    context = {
        "boolean":True,
        "message":"Message Sent Successfully",
        
    }
    return JsonResponse({
        "data":context
    })









def aboutUsView(request):
    return render(request , "core/about-us.html")


def purchaseGuideView(request):
    return render(request , "core/purchase-guide.html")

def privacyPolicyView(request):
    return render(request , "core/privacy-policy.html")

def termsOfServiceView(request):
    return render(request , "core/terms-of-service.html")













# def addToWishlist(request):
#     id = request.GET['id']
#     product = Product.objects.get(id=id)
#     wishlist_count = Wishlists.objects.filter(user=request.user , product=product).count()
#     context = {}
#     if wishlist_count > 0 :
#         context = {
#             "boolean" : True
#         }
#     else :
#         new_wishlist = Wishlists.objects.create(user=request.user , product=product)
#         context = {
#                 "boolean" : True
#             }
#     return JsonResponse(context)