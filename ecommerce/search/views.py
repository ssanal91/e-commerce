from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

def search(request):

    if(request.method=="POST"):
        p=None
        q=""
        query=request.POST['q']
        # print(query)
        if(query):
            p=Product.objects.filter(Q(name__icontains=query)|Q(desc__icontains=query))

    return render(request,'search.html',{'p':p,'q':query})
