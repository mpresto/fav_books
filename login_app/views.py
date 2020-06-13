from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.


def index(request):
    # login / registration page
    # redirect to books/
    return render(request, 'login/index.html')

def login(request):
    # validate login credentials
    user = User.objects.filter(email=request.POST['email'])  # check if user in db
    if user:  # if user returned
        logged_user = user[0]
        # check password match
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['username'] = logged_user.first_name  # save user info in sessions
            request.session['user_id'] = logged_user.id
            return redirect('/books')  # if match, redirect to success page
    # if we didn't find a match, display errors, redirect to login page
    messages.error(request, "Email and password do not match.")
    return redirect('/')


def register(request):
        # validate registration form info
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:  # if no errors, create new user
        # hash password:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)

        new_user = User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            password=pw_hash
        )
        messages.success(request, "Registration successful!")
        print("Created a new user")
        request.session['username'] = new_user.first_name  # save user info in sessions
        request.session['user_id'] = new_user.id
        # redirect to a success route
        return redirect('/books')

def logout(request):
    # logout (clear session) and redirect to login page
    request.session.flush()
    return redirect('/')