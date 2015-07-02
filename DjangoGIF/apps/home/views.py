from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from ..users.models import Profile
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'home/home.html')


def login_view(request):
    logged_in = False
    if request.user.is_authenticated():
        logged_in = True

    context = {
        'form': LoginForm(),
        'logged_in': logged_in,
        'username': request.user.username
        }
    return render(request, 'home/login.html', context)


def logout_view(request):
    logout(request)
    context = {'message': 'You have been succesfully logged out!'}
    return render(request, 'home/home.html', context)


def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/u/%s' % str(user.username))
        else:
            context = {
                'form': LoginForm(),
                'message': 'This account has been deactivated, please create a new one.'
            }
            return render(request, 'home/login.html', context)
    else:
        context = {
            'form': LoginForm(),
            'message': 'Invalid Login, please try again.'
        }
        return render(request, 'home/login.html', context)


def signup(request):
    print request.user.username
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            message = 'Account Created!'
            print message
    else:
        form = SignupForm()
    return render(request, 'home/signup.html', {'form': form})


def create_account(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            firstname = request.POST['first_name']
            u = User.objects.create_user(username=username, password=password, email=email, first_name=firstname)
            p = Profile(owner=u)
            u.save()
            p.save()
            request.user.username = username
            context = {
                'name': firstname,
                'username': username
            }
            return render(request, 'home/account_created.html', context)
        else:
            context = {
                'form': form
            }
            return render(request, 'home/signup.html', context)
    else:
        form = SignupForm()
        return render(request, 'home/signup.html', {'form': form})