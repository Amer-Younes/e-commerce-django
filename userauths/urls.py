
from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="userauths"

urlpatterns = [
    path("sign-up/", views.registerView , name = "sign-up" ) , 
    path("sign-in/", views.loginView , name = "sign-in" ) , 
    path("sign-out/", views.logoutView , name = "sign-out" ) , 
    path("profile/edit/", views.profileEditView , name = "profile-edit" ) , 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)