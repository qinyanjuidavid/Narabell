from django.shortcuts import render
from django.http import HttpResponse
from myapp.forms import BookForm
from myapp.models import Book


def home(request):
    book=Book.objects.all()
    context={
    'book':book
    }
    return render(request,'myapp/home.html',context)


def upload(request):
    if request.method=="POST":
        form=BookForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            form=BookForm()
    else:
        form=BookForm()
    context={
    'form':form
    }
    return render(request,'myapp/upload.html',context)
