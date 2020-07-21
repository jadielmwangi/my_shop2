
from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()##you create a new order in the database using order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})




# def musician_list(request):
#     MUSICIANS = [
#         {'name': 'Django Reinhardt', 'genre': 'jazz'},
#         {'name': 'Jimi Hendrix',    'genre':'rock'},
#         {'name': 'Louis Armstrong', 'genre': 'jazz'},
#         {'name': 'Pete Townsend', 'genre': 'rock'},
#     ]

#     return render('musician_list.html', {'musicians': MUSICIANS})                  

