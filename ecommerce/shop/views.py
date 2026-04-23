from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout,login,authenticate
from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from django.contrib import messages
from shop.forms import SignUpForm, LoginForm
from shop.models import Category



# Create your views here.
class Categoryview(View):
    def get(self, request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request, 'category.html',context)
class Products(View):
    def get(self, request,i):
        c = Category.objects.get(id=i)
        context = {'category': c}
        return render(request, 'product.html',context)

class Login(View):
    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html',context)
    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data
            u = data['username']
            p = data['password']
            user = authenticate(username=u, password=p)
            if user and user.is_superuser == True:
                login(request, user)
                return redirect('shop:home')
            elif user:
                login(request, user)
                return redirect('shop:home')
            else:
                messages.error(request, 'Username or password is incorrect')
                return redirect('shop:login')

class Register(View):
    def get(self, request):
        form_instance = SignUpForm()
        context = {'form': form_instance}
        return render(request, 'register.html',context)
    def post(self, request):
        form_instance = SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:login')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('shop:login')
from shop.forms import ProductForm,CategoryForm
class Addproduct(View):
    def get(self, request):
        form_instance = ProductForm()
        context = {'form': form_instance}
        return render(request, 'addproduct.html',context)
    def post(self, request):
        form_instance = ProductForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:home')
class Addcategory(View):
    def get(self, request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategory.html',context)
    def post(self, request):
        form_instance = CategoryForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
        return redirect('shop:home')
from shop.models import Product
class Detail(View):
    def get(self, request,i):

        p = Product.objects.get(id=i)
        context = {'product': p}
        return render(request, 'detail.html',context)
from shop.forms import StockForm
class Addstock(View):
    def post(self, request, i):
        p = Product.objects.get(id=i)
        form_instance = StockForm(request.POST, request.FILES, instance=p)

        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:home')

    def get(self, request, i):
        p = Product.objects.get(id=i)
        form_instance = StockForm(instance=p)
        context = {'form': form_instance}
        return render(request, 'addstock.html', context)



