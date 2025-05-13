
from django.urls import path , include
from . import views

app_name="core"

urlpatterns = [
    # HomePage
    path('', views.index  , name="index" ) , 
    path('products/', views.productListView  , name="product-list" ) , 

    # Category
    path('category/', views.categoryListView  , name="category-list" ) , 
    path('category/<cid>/', views.categoryProductListView  , name="category-product-list" ) , 

    # Vendor
    path('vendors/', views.vendorListView  , name="vendor-list" ) , 
    path('vendor/<vid>/', views.vendorDetailView  , name="vendor-detail" ) , 

    # Product
    path('product/<pid>/', views.productDetailView  , name="product-detail" ) , 

    # Tags
    path('products/tag/<slug:tag_slug>/', views.tagList  , name="tags" ) , 


    # Add Review
    path('ajax-add-review/<pid>/', views.ajaxAddReview  , name="ajax-add-review" ) , 


    # Search
    path('search/', views.searchView  , name="search" ) , 

    # Filter
    path('filter-products/', views.filterProductView  , name="filter-product" ) , 


    # Cart
    path('cart/', views.cartView  , name="cart" ) , 
    path('add-to-cart/', views.addToCartView  , name="add-to-cart" ) , 
    path('delete-from-cart/', views.deleteFromCartView  , name="delete-from-cart" ) , 
    path('update-cart/', views.updateProductFromCartView  , name="update-cart" ) , 


    # Checkout
    path('checkout/<oid>', views.checkoutView  , name="checkout" ) , 


    # PayPal
    path('paypal/',include('paypal.standard.ipn.urls') ) , 


    # Payment
        # paypal
    path('payment-completed/<oid>/', views.paymentCompleteView  , name="payment-completed" ) , 
    path('payment-failed/', views.paymentFailedView  , name="payment-failed" ) , 
        # stripe
    path('api/create_checkout_session/<oid>/', views.createCheckoutSession  , name="create_checkout_session" ) ,

    # Customer Dashboard
    path('dashboard/', views.customerDashboardView  , name="dashboard" ) , 


    # Order Detail
    path('dashboard/order/<id>', views.order_detail  , name="order-detail" ) , 


    # Making Address Default
    path('make-default-address/', views.defaultAddress  , name="make-default-address" ) , 


    #  Wishlist
    path('wishlist/', views.wishlistPageView  , name="wishlist" ) , 
    path('toggle-wishlist/', views.toggleWishlist  , name="toggle-wishlist" ) , 
    path('delete-product-from-wishlist/', views.deleteFromWishlistView  , name="delete-product-from-wishlist" ) , 


    # Contact
    path('contact/', views.contactView  , name="contact" ) , 
    path('contact-us/', views.ajaxContactView  , name="contact-us" ) , 


    # New Routes
    path('save-checkout-info/', views.saveCheckoutInfo  , name="save-checkout-info" ) , 


    # # Add To Wishlist
    # path('add-to-wishlist/', views.addToWishlist  , name="add-to-wishlist" ) , 
]