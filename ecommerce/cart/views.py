from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Product

from django.http import HttpResponse

from cart.models import Cart,Account,Order1


@login_required()
def cart_view(request):
    #for displaying cart
    total=0
    u=request.user
    c=Cart.objects.filter(user=u)
    for i in c:# sequence c,i is each object in c sequenceFor getting totl amount and to display in page
        total=total+i.quantity*i.product.price
        #for passing value of total will give in context

    return render(request, 'cart.html',{'c':c,'total':total})



@login_required()
def addtocart(request,p):
    #for adding a particular product to cart

    p=Product.objects.get(id=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity+=1
            cart.save()
            p.stock-=1 # product add cheyumbo stock minus vanam
            p.save()
    except:
        if (p.stock > 0):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1  # product add cheyumbo stock minus vanam
            p.save()

    # return render(request,'cart.html')
    return cart_view(request)

def cart_remove(request,p):

    p=Product.objects.get(id=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)

        if(cart.quantity > 1):
            cart.quantity-=1
            cart.save()
            p.stock += 1  # product add cheyumbo stock minus vanam
            p.save()
        else:
            cart.delete()
            p.stock+=1
            p.save()

    except:
        pass
    return cart_view(request)

def cartdelete(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock+= cart.quantity
        p.save()
    except:
        pass
    return cart_view(request)

@login_required()
def orderform(request):
    if(request.method == "POST"):
        a=request.POST['a']
        p=request.POST['p']
        an=request.POST['an']
    #     #for ading payment need to know the cart products and hu us the user
        u=request.user
    #     #then a personinte cartile details get cheyyanam
    #
        c=Cart.objects.filter(user=u)
    #
        total=0
        for i in c:
            total=total+i.quantity*i.product.price

        try:
            ac=Account.objects.get(acctnum=an)
            if(ac.amount >= total):
                ac.amount=ac.amount-total
                ac.save()
                for i in c:
                    o=Order1.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()

                c.delete()
                msg="Order Placesd Sucessfully"
                # return render(request,'orderform.html',{'message':msg})
                return render(request, 'orderdetails.html', {'message': msg})
            else:

                msg="Insufficient Amount,Cannot place your order"
                # return render(request, 'orderform.html', {'message': msg})
                return render(request, 'orderform.html', {'message': msg})

        except:
            pass

    return render(request,'orderform.html')

def yourorder(request):
    u=request.user
    o=Order1.objects.filter(user=u)



    return render(request,'orderedviews.html',{'o':o,'u':u.username})
