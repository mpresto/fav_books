from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect

from django.contrib import messages
from . import views
from .models import Book
from login_app.models import User


# Create your views here.

def index(request):
    if 'user_id' not in request.session:  # send back to login
        return redirect('/login')
    context = {
        'all_books': Book.objects.all(),
        'logged_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'book/index.html', context)


def add_book(request):
    # check for errors:
    errors = Book.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        # create a book instance:
        logged_user = User.objects.get(id=request.session['user_id'])
        new_book = Book.objects.create(
            uploaded_by=logged_user,
            title=request.POST['title'],
            desc=request.POST['desc'],
        )
        print("Created new book.")
        messages.success(request, "Added new book!")
        # add to user's favorites:
        new_book.liked_by.add(logged_user)
    # redirect to homepage
    return redirect(f'/books/{new_book.id}')


def book_detail(request, id):
    # render book detail page
    context = {
        'this_book': Book.objects.get(id=id),
        'logged_user': User.objects.get(id=request.session['user_id']),
        'all_users': User.objects.all()
    }
    return render(request, 'book/book_detail.html', context)


def update_book(request, id):
    this_book = Book.objects.get(id=id)
    # check for errors:
    errors = Book.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        # update book instance:
        this_book.title=request.POST['title']
        this_book.desc=request.POST['desc']
        this_book.save()
        messages.success(request, "Successfully updated book!")

        # add to user's favorites:
    # redirect to homepage
    return redirect(f'/books/{this_book.id}')


def delete_book(request, id):
    this_book = Book.objects.get(id=id)
    this_book.delete()
    messages.success(request, "Book has been deleted")
    return redirect('/books')


def add_favorite(request, id):
    # create favorite relationship
    logged_user = request.session['user_id']
    this_book = Book.objects.get(id=id)
    this_book.liked_by.add(logged_user)
    print("added to favorites")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))




def remove_favorite(request, id):
    # remove favorite relationship
    logged_user = request.session['user_id']
    this_book = Book.objects.get(id=id)
    this_book.liked_by.remove(logged_user)
    print("removed from favorites")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def user_detail(request, id):
    # render user detail page
    context = {
        'logged_user': User.objects.get(id=id),
        'all_books': Book.objects.all()
    }
    return render(request, 'book/user_detail.html', context)




