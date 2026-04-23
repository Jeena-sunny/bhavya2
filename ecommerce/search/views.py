
from shop.models import Product
from django.db.models import Q
from django.views import View
from django.shortcuts import render,redirect
class Search(View):
    def get(self,request):
        query = request.GET['q']
        print(query)
        b = Product.objects.filter(Q(name__icontains=query)|
                                Q(price__icontains=query)|

                                Q(discription__icontains=query))




        context = {'products':b}
        return render(request,'search.html',context)
