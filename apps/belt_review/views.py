from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
def index(request): #index page
    return render(request, 'index.html')

def books(request): #user home page
    if 'id' not in request.session:
        return redirect('/')
    else:
        books_data = Book.objects.all()
        review_data = Review.objects.all().order_by("-created_at")
        user_data= User.objects.all().values()
        context = {
            'books':books_data,
            'reviews': review_data[:3],
            'user': user_data,
        }
        return render(request, 'books.html', context)

def add(request):#add book and review page
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'books_data':Book.objects.all()
        }
        return render(request, 'add.html', context)

def review(request,id): #add review to existing book on ID page
    if 'id' not in request.session:
        return redirect('/')
    else:
        book_data = Book.objects.get(id=id)
        review_data = Review.objects.filter(books_id=id)
        user_data= User.objects.all().values()
        session_id=request.session['id']
        context = {
            'books':book_data ,
            'reviews': review_data,
            'user': user_data,
            'session_id':session_id
        }
        return render(request, 'review.html', context)

def user(request, id): #shows user info and posted reviews page
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'data': User.objects.get(id=id),
            'reviews': Review.objects.filter(users_id=id).order_by("-created_at"),
            'review_count': Review.objects.filter(users_id=id).order_by("-created_at").count(),
            'session_id': request.session['id'],
        }
        return render(request, 'user.html', context)

def add_br(request): #add book and review
    if request.method == "POST":
        errors3 = Book.objects.validator3(request.POST)
        if 'success' in errors3:
            this_id = request.session['id']
            author = errors3['success']
            new_book = Book.objects.create(book_title=request.POST['title'], author=author, uploaded_by_id=this_id)
            Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], users_id=this_id, books_id=new_book.id)
            return redirect('/books')
        else:
            for tag, error in errors3.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/add')
    else:
        return redirect('/books/add')

def add_r(request):
    if request.method == "POST":
        errors4=Book.objects.validator4(request.POST)
        book_id = request.POST['add_book_id']
        if 'success' in errors4:
            this_id = request.session['id']
            Review.objects.create(review=request.POST['add_review'], rating=request.POST['add_rating'], users_id=this_id, books_id=book_id)
            return redirect('/books/'+book_id)
        else:
            for tag, error in errors4.iteritems():
                messages.error(request, error, extra_tags=tag)
                return redirect('/books/'+book_id)
    else:
        return redirect('/books/'+book_id)

def delete_r(request,id,id2):
        print "bob"
        book_id=id
        review_id=id2
        delete_r = Review.objects.get(id=review_id)
        delete_r.delete()
        return redirect('/books/'+book_id)

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if 'valid_user' in errors:
            request.session['register_email']=request.POST['email']
            request.session['name'] =errors['valid_user'].name
            request.session['id']= errors['valid_user'].id
            return redirect('/books')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        errors2 = User.objects.validator2(request.POST)
        if 'success' in errors2:
            request.session['name'] = errors2['success'].name
            request.session['email'] = errors2['success'].email
            request.session['id']= errors2['success'].id
            return redirect('/books')
        else:
            for tag, error in errors2.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
