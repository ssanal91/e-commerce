from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

def allcategories(request):
    #for displaying all categories
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})


def allproducts(request,p):
    #for displaying all categories
    c = Category.objects.get(id=p)
    p=Product.objects.filter(category=c)

    return render(request,'product.html',{'c':c,'p':p})
@login_required()
def showdetails(request,p):
    p=Product.objects.get(id=p)
    return render(request,'details.html',{'p':p})

def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']

        if(cp==p):
            user=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            user.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Passwords are not match")

    return render(request,'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)

        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'Login.html')


@login_required()
def user_logout(request):
    logout(request)
    return allcategories(request)