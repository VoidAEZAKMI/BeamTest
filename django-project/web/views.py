from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse


def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']

        product = Product.objects.create(name=name, price=price)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Новый продукт "{product.name}" был создан!'
            }
        )

        return JsonResponse(
            {'success': True, 'product_name': product.name, 'product_price': product.price, 'product_id': product.id})

    return JsonResponse({'success': False})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        old_name = product.name
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Продукт "{old_name}" был обновлён на "{product.name}"!'
            }
        )

        return JsonResponse(
            {'success': True, 'product_id': product.id, 'product_name': product.name, 'product_price': product.price})

    return JsonResponse({'success': False})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Продукт "{product_name}" был удалён!'
            }
        )

        return JsonResponse({'success': True, 'product_id': pk})

    return JsonResponse({'success': False})
