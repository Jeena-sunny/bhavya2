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
class Category(View):
    def get(self, request):
        c=Category.objects.all()
        context={'category':c}
        return render(request, 'category.html',context)


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
                return redirect('shop:category')
            elif user:
                login(request, user)
                return redirect('shop:category')
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