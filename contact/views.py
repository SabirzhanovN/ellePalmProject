from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, History
from shop.models import Catalog, Category, Product, Color, Size

from shop.views import catalogs_categories_for_menu, get_cart_favorites
from .service import send_message_bot


def contact(request):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    lst = catalogs_categories_for_menu()

    context = {
        'head_cat': lst,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len
    }
    return render(request, 'contact/contact.html', context)


# Отправка уведомлении при заказе с корзины(несколько товаров за раз)
def make_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        region = request.POST.get('region')
        address = request.POST.get('address')
        home = request.POST.get('home')
        apartment = request.POST.get('apartment')
        delivery = request.POST.get('delivery')
        message = request.POST.get('message')

        # Пустая строка для отправки смс в телеграм(далее заполнится)
        products = ""
        summary_price = 0
        cart = Cart.objects.filter(user=request.user.id)
        history = History.objects.create(
            first_name=first_name,
            last_name=last_name,
            second_name=second_name,
            email=email,
            phone=phone,
            address=f"{region} {address} {home} {apartment}",
            delivery=delivery,
            total_count=0,
            total_price=0
        )

        for product in cart:
            # Обьект корзины для привзки заказа к истории заказов
            temp_cart = Cart.objects.create(
                product=product.product,
                color=product.color,
                size=product.size,
                total_count=product.total_count,
                total_price=product.total_price
            )

            temp_cart.save()
            history.products.add(temp_cart.id)
            history.total_count += 1

            summary_price += product.total_price
            products += f"""
            \tТовар: {product.product.category.name}/{product.product.name}
            \t\t-Количество: {product.total_count}
            \t\t-Цвет: {product.color}
            \t\t-Размер: {product.size}
            \t\t-Стоимость: {product.product.price}сом/{product.total_price}сом
            """

        history.total_price += summary_price
        history.save()

        order = f"""
        Заказ с сайта *
        _____________
        ФИО: {last_name} {first_name} {second_name}
        Email: {email}
        Номер: {phone}
        Адрес: {region}/{address}, дом: {home}, кв:{apartment}
        Способ: {delivery}
        Сообщение: {message}
        ____________
        Детали: {products}
        ____________
        Общая стоимость: {summary_price} сом
        """

        send_message_bot(order)
        messages.success(request, "Ваш заказ принят, ожидайте :)")
        return redirect("home")

    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    lst = catalogs_categories_for_menu()

    context = {
        'head_cat': lst,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len
    }
    return render(request, 'contact/make_order.html', context)


def make_order_single(request, id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        region = request.POST.get('region')
        address = request.POST.get('address')
        home = request.POST.get('home')
        apartment = request.POST.get('apartment')
        delivery = request.POST.get('delivery')
        message = request.POST.get('message')

        color = request.POST.get('color')
        size = request.POST.get('size')

        product = get_object_or_404(Product, id=id)
        product_detail = f"""
        \tТовар: {product.name}
        \t\t-Количество: 1
        \t\t-Цвет: {get_object_or_404(Color, id=color).color}
        \t\t-Размер: {get_object_or_404(Size, id=size).size}
        \t\t-Стоимость: {product.price} сом
        """

        history = History.objects.create(
            first_name=first_name,
            last_name=last_name,
            second_name=second_name,
            email=email,
            phone=phone,
            address=f"{region} {address} {home} {apartment}",
            delivery=delivery,
            total_count=1,
            total_price=product.price,
        )
        # Обьект корзины для привзки заказа к истории заказов
        temp_cart = Cart.objects.create(
            product=product,
            color=get_object_or_404(Color, id=color),
            size=get_object_or_404(Size, id=size),
            total_price=product.price,
            total_count=1
        )
        temp_cart.save()
        history.products.add(temp_cart.id)
        history.save()

        order = f"""
        Заказ с сайта *
        _____________
        ФИО: {last_name} {first_name} {second_name}
        Email: {email}
        Номер: {phone}
        Адрес: {region}/{address}, {home}{apartment}
        Способ: {delivery}
        Сообщение: {message}
        ____________
        Детали: {product_detail}
        """

        send_message_bot(order)
        messages.success(request, "Ваш заказ принят, ожидайте :)")
        return redirect('home')

    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    lst = catalogs_categories_for_menu()
    product = get_object_or_404(Product, id=id)

    context = {
        'product': product,
        'head_cat': lst,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len
    }

    return render(request, 'contact/make_order_single.html', context)


# обратный звонок с формы index.html, contact.html
def call_back(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        call_back_message = f"""
        Обратный звонок *
        ________________
            Ф.И.О: {full_name}
            Номер: {phone}
            Почта: {email}
            Сообщение: {message}
        """
        send_message_bot(call_back_message)

        messages.success(request, "Заявка на обратный звонок")
        return redirect('home')
    return redirect('home')


def privacy_policy(request):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    lst = catalogs_categories_for_menu()

    context = {
        'head_cat': lst,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'fav_len': fav_len
    }

    return render(request, 'contact/privacy_policy.html', context)

