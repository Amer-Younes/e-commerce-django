from .models import Product , Category , Vendor , CartOrder , CartOrderItem , ProductImages , Wishlists , Address , ProductReview 
from django.db.models import Min,Max










def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price") , Max("price"))

    try:
        wishlistCount= Wishlists.objects.filter(user=request.user).count()
    except:
        wishlistCount = 0

    try:
        user_wishlist = Wishlists.objects.filter(user=request.user).values_list('product_id', flat=True)
    except:
        user_wishlist =None

    try:
        address = Address.objects.get(user = request.user)
        
    except:
        address = None

    return {
        'categories':categories , 
        'address':address , 
        'vendors':vendors , 
        'min_max_price':min_max_price , 
        'wishlistCount':wishlistCount , 
        'user_wishlist':user_wishlist , 

    }
