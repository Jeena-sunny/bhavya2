import uuid

from django.db import models
from django.forms.utils import to_current_timezone
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
import razorpay
from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product

from cart.forms import OrderForm


# Create your views her
class Addtocart(View):
    def get(self,request,i):
        u=request.user    #login chytha user arannannu viewvil kittan
        p=Product.objects.get(id=i)   #ethu product user eduthu

        #product user already select chythitondoo ennu ariyan
        try:
            c=Cart.objects.get(user=u,product=p)   #userthe peril agganathe oru product ondoo
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')
class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        # total
        total=0

        for i in c:
            total=total+(i.quantity*i.product.price)

        context={'cart':c,'total':total}
        return render(request,'addtocart.html',context)

class CartDecrement(View):
    def get(self, request, i):
        try:
            c = Cart.objects.get(id=i)

            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()

        except:
            pass

        return redirect('cart:cartview')
class CartRemove(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)

            c.delete()
        except:
            pass
        return redirect('cart:cartview')
import uuid
class Checkout(View):
    def get(self,request):
        form_instance = OrderForm()
        context = {'form':form_instance}
        return render(request,'checkout.html',context)
    def post(self,request):
        form_instance = OrderForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)
            #user
            user= request.user
            u.user=user
            #total amount
            c = Cart.objects.filter(user=user)
            total = 0
            for i in c:
                total = total + (i.quantity*i.product.price)
            u.amount=total
            u.save()
            if u.payment_method=='online':
                # create a razorpay client connection using key
                client = razorpay.Client(auth=('rzp_test_SfoSubtFyxy2Zb','fTeksQetvfG43UQRFlSil03d'))
                # create a new order in razorpay
                response_payment = client.order.create({
                    'amount': int(u.amount * 100),
                    'currency': 'INR'
                })
                print(response_payment)
                # retrive the order id from response payment
                oid=response_payment['id']
                # add order id in our db table
                u.order_id=oid
                u.save()
                context = {'payment':response_payment}
                return render(request, 'payment.html', context)

            else:#COD
                id=uuid.uuid4().hex[:14]
                i='order_COD'+id
                u.order_id=i
                u.is_ordered = True
                u.save()

                # cart
                c=Cart.objects.filter(user=user)
                for i in c:
                    items=OrderItems.objects.create(order=u,product=i.product,quantity=i.quantity)
                    items.save()
                c.delete()
                return render(request,'payment.html')
from .models import Order, OrderItems

@method_decorator(csrf_exempt,name='dispatch')
class PaymentSuccess(View):
    def post(self, request):
        response=request.POST
        print(response)

        # after successful payment mark order as True


        id = response['razorpay_order_id']
        o = Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()

        c=Cart.objects.filter(user=o.user)
        for i in c:
            items=OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity)
            items.save()

        #deletes the cart
        c.delete()


        return render(request, 'paymentsucess.html')

class Ordersummary(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'ordersummary.html',context)






