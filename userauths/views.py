# from django.shortcuts import redirect, render
# from .forms import UserRegisterForm
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from userauths.models import User


# # Register View
# def registerView(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)  # No need for 'or None'
#         if form.is_valid():
#             new_user = form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request, f"Hey {username}, your account was created successfully.")
            
#             # Authenticate and log the user in immediately after registration
#             new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
#             if new_user:
#                 login(request, new_user)
#                 return redirect("core:index")
#         else:
#             messages.warning(request, "There was an error with your registration form.")
#     else:
#         form = UserRegisterForm()

#     context = {
#         'form': form,
#     }
#     return render(request, "userauths/sign-up.html", context)


# # Login View
# def loginView(request):
#     if request.user.is_authenticated:
#         messages.warning(request, "You are already logged in.")
#         return redirect("core:index")

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Authenticate the user using the email and password
#         user = authenticate(request, username=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             messages.success(request, "You logged in successfully.")
#             return redirect("core:index")
#         else:
#             messages.warning(request, "Invalid credentials. Please try again or create an account.")

#     return render(request, "userauths/sign-in.html")


# # Logout View
# def logoutView(request):
#     logout(request)
#     messages.success(request, "You logged out successfully.")
#     return redirect("userauths:sign-in")




from django.shortcuts import redirect, render
from .forms import UserRegisterForm , ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from userauths.models import User , Profile
from django.contrib.auth.decorators import login_required


# Register View
def registerView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)  # No need for 'or None'
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
            
            # Authenticate and log the user in immediately after registration
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            if new_user:
                login(request, new_user)
                return redirect("core:index")
        else:
            messages.warning(request, "There was an error with your registration form.")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)








# Login View
def loginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user using the email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You logged in successfully.")
            return redirect("core:index")
        else:
            messages.warning(request, "Invalid credentials. Please try again or create an account.")

    return render(request, "userauths/sign-in.html")





# Logout View
def logoutView(request):
    logout(request)
    messages.success(request, "You logged out successfully.")
    return redirect("userauths:sign-in")


def profileEditView(request):
    profile = request.user.profile  # Get the profile instance for the logged-in user
    form = ProfileUpdateForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("core:dashboard")
        else:
            messages.warning(request, "There was an error with your form.")
    
    context = {
        "form": form,
        "profile": profile,  # Pass profile to template for easy access
    }
    return render(request, "userauths/profile-edit.html", context)
