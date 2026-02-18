from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
# Create your views here.


def home_view(request):
    return render(request, "home.html")


def connexion_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        form.is_valid()
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = AuthenticationForm()
    return render(request, "connexion.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blogapp:home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# def register_view(request):
#    if request.method == 'POST':
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request,'home.html')


#     return render(request,'register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("blogapp:home")
