from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUp, EditProfileForm
# Create your views here.
def home(request):
    return render(request,'cs382leave/home.html',{})

def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        users = authenticate(request,username=username,password=password)
        if users is not None:
            login(request, users)
            messages.success(request, ('You have logged In!'))
            return redirect('home')
        else:
            messages.success(request, ('Error Logging-In, Please Try Again...'))
            return redirect('login')

    else:
        return render(request,'cs382leave/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have logged out'))
    return redirect('home')


def register_user(request):
    if request.method=="POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request,('You have registered....'))
            return redirect('home')
    else:
            form=SignUp()
    context = {'form':form}
    return render(request, 'cs382leave/registration.html', context)


def edit_profile(request):
    if request.method=="POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,('You have Edited your profile'))
            return redirect('home')
    else:
            form=EditProfileForm(instance = request.user)
    context = {'form':form}
    return render(request, 'cs382leave/edit_profile.html', context)


def change_password(request):
    if request.method =='POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,('You have changed your Password'))
            return redirect('home')
    else:
        form = PasswordChangeForm(user = request.user)

    context = {'form': form}

    return render(request, 'cs382leave/change_password.html', context)


def application_form(request):
    return render(request, 'cs382leave/application_form.html', {})
