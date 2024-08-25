from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Customer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    customers = Customer.objects.all()
    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'customers': customers
    })


def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        category_id = request.POST['category']

        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(name=name, price=price)
        product.categories.add(category)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Новый продукт "{product.name}" в категории "{category.name}" был создан!'
            }
        )

        return JsonResponse(
            {'success': True, 'product_name': product.name, 'product_price': product.price, 'product_id': product.id, 'category_name': category.name, 'category_id': category.id})

    return JsonResponse({'success': False})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        old_name = product.name
        product.name = request.POST['name']
        product.price = request.POST['price']
        category_id = request.POST['category']

        category = get_object_or_404(Category, id=category_id)
        product.categories.set([category])
        product.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Продукт "{old_name}" был обновлён на "{product.name}" в категории "{category.name}"!'
            }
        )

        return JsonResponse(
            {'success': True, 'product_id': product.id, 'product_name': product.name, 'product_price': product.price, 'category_name': category.name, 'category_id': category.id})

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

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        name = request.POST['name']

        category = Category.objects.create(name=name)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Новая категория "{category.name}" была создана!'
            }
        )

        return JsonResponse({'success': True, 'category_name': category.name, 'category_id': category.id})

    return JsonResponse({'success': False})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        old_name = category.name
        category.name = request.POST['name']
        category.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Категория "{old_name}" была обновлена на "{category.name}"!'
            }
        )

        return JsonResponse({'success': True, 'category_id': category.id, 'category_name': category.name})

    return JsonResponse({'success': False})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Категория "{category_name}" была удалена!'
            }
        )

        return JsonResponse({'success': True, 'category_id': pk})

    return JsonResponse({'success': False})