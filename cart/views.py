from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, Color, Size
from shop.views import get_cart_favorites, catalogs_categories_for_menu
from .models import Cart, Favorite
from django.contrib import messages


# Для кнопки(сердце) в product_detail.html
def add_to_favorites(request, id):
    favorite = Favorite.objects.create(
        user=request.user,
        product=Product.objects.get(id=id)
    )

    favorite.save()

    messages.success(request, 'Добавлено в избранные')

    return redirect('product_detail', id)


def delete_from_favorites(request, id):
    favorite_id = Favorite.objects.get(user=request.user.id, product=Product.objects.get(id=id)).id
    Favorite.objects.get(id=favorite_id).delete()

    messages.success(request, "Удалено с избранных")

    return redirect('product_detail', id)


def favorites_list(request):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    catalogs_categories = catalogs_categories_for_menu()

    favorite_products = Favorite.objects.filter(user=request.user.id)

    context = {
        "head_cat": catalogs_categories,
        "favorite_products": favorite_products,

        "cart": cart,
        "cart_count": cart_count,
        "total_price": total_price,

        "favorites": favorites,
        "fav_len": fav_len,
    }

    return render(request, "favorites/favorites.html", context)


def add_to_cart(request, id):
    color_id = request.POST.get('color')
    size_id = request.POST.get('size')

    # Если каким-то образом с формы пришла цифра 0 или отрицательное число
    count = 1 if int(request.POST.get('count')) <= 0 else request.POST.get('count')

    user = request.user
    product = get_object_or_404(Product, id=id)

    cart = Cart.objects.create(
        user=user,
        product=product,
        total_count=count,
        total_price=product.price * int(count),
        color=Color.objects.get(id=int(color_id)),
        size=Size.objects.get(id=int(size_id))
    )

    cart.save()
    messages.success(request, 'Товар добавлен в корзину')

    return redirect('product_detail', id)


def edit_cart(request):
    if request.method == 'POST':
        cart_ids = request.POST.getlist('ids')
        numbers = request.POST.getlist('number')
        sizes = request.POST.getlist('size')
        colors = request.POST.getlist('color')

        for i in range(len(cart_ids)):
            cart = get_object_or_404(Cart, id=cart_ids[i])
            cart.total_count = numbers[i]
            cart.size = Size.objects.get(id=sizes[i])
            cart.color = Color.objects.get(id=colors[i])
            cart.total_price = int(cart.product.price) * int(numbers[i])

            cart.save()

        messages.success(request, 'Корзина обновлена')
        return redirect('edit_cart')

    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    catalogs_categories = catalogs_categories_for_menu()

    context = {
        'head_cat': catalogs_categories,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len
    }

    return render(request, 'cart/cart_page_edit.html', context)


def delete_cart(request, id):
    Cart.objects.get(id=id).delete()
    messages.success(request, "Товар удален с корзины")

    return redirect('edit_cart')


# Удаление всех товаров в корзине
def delete_all_cart(request):
    carts = Cart.objects.filter(user=request.user.id)
    for cart in carts:
        cart.delete()

    messages.success(request, 'Корзина очищен')

    return redirect('edit_cart')
