from django.urls import path
from . import views


app_name="useradmin"


urlpatterns = [
    path('dashboard/', views.dashboard  , name="dashboard" ) ,
    path('products/', views.products  , name="products" ) ,
    path('add-product/', views.addProductView  , name="add-product" ) ,
    path('edit-product/<pid>', views.editProductView  , name="edit-product" ) ,
    path('delete-product/<pid>', views.deleteProductView  , name="delete-product" ) ,
    path('orders/', views.orders  , name="orders" ) ,
    path('order/<id>/', views.orderDetails  , name="order-detail" ) ,
    path('order/update-status/<id>/', views.updateOrderStatus , name='update_order_status'),
    path('shop/', views.shopPage , name='shop'),
    path('reviews/', views.reviews , name='reviews'),
    path('settings/', views.settings , name='settings'),
    path('change-password/', views.changePassword , name='change-password'),






]