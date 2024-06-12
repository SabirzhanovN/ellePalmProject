from django.shortcuts import render, get_object_or_404

from cart.models import Cart, Favorite
from .models import Catalog, Category, Product
from django.core.paginator import Paginator


# Создание словаря из катологов и к ним относящися категории для отображения в меню
def catalogs_categories_for_menu():
    catalogs = Catalog.objects.all()

    result = []
    for cat in catalogs:
        dict_of_catalogs_category = {
            "catalog": cat,
            "categories": Category.objects.filter(catalog=cat)
        }

        result.append(dict_of_catalogs_category)

    return result


# Получение всех избранных и товаров с корзины если пользователь авторизован
def get_cart_favorites(user):
    if str(user) != 'AnonymousUser':
        cart = Cart.objects.filter(user=user.id)
        cart_count = len(cart)
        total_price = sum([int(i.total_price) for i in cart])
        favorites = Favorite.objects.filter(user=user.id)
        favorites = [str(i) for i in favorites]
        fav_len = len(favorites)
    else:
        cart, cart_count, total_price, favorites,fav_len = None, None, None, None, None

    return [cart, cart_count, total_price, favorites, fav_len]


def index(request):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)

    catalogs = Catalog.objects.all()
    products = Product.objects.order_by("-date_of_public")

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    catalogs_categories = catalogs_categories_for_menu()

    data = {
        "head_cat": catalogs_categories,
        "catalogs": catalogs,
        "products": page_obj,

        "cart": cart,
        "cart_count": cart_count,
        "total_price": total_price,

        "favorites": favorites,
        "fav_len": fav_len
    }
    # Для кнопки "Больше", загрузка товаров без обновлении страницы
    if request.htmx:
        return render(request, 'blocks/list_products_index.html', data)

    return render(request, 'shop/index.html', data)


# Вывод списка товаров относящиеся к 1 катологу (при нажатии из меню)
def listing_products_by_catalog(request, slug):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)

    if slug != "all":
        catalog = get_object_or_404(Catalog, slug=slug)
        categories = Category.objects.filter(catalog=catalog.id)
        cat_ids = [i.id for i in categories]
        products_all = Product.objects.all()

        products = []
        for product in products_all:
            if product.category.id in cat_ids:
                products.append(product)
    else:
        catalog = "all"
        categories = Category.objects.all()
        products = Product.objects.all()

    catalogs_categories = catalogs_categories_for_menu()

    cnt_products = len(products)
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {
        "catalog": "Все товары" if catalog == "all" else catalog,
        "categories": categories,
        "products": page_obj,
        "head_cat": catalogs_categories,
        "cnt_products": cnt_products,

        "cart": cart,
        "cart_count": cart_count,
        "total_price": total_price,

        "favorites": favorites,
        "fav_len": fav_len
    }

    if request.htmx:
        return render(request, 'blocks/list_products_listing_products_by_catalog.html', data)

    return render(request, 'shop/listing_products_by_catalog.html', data)


# Вывод списка товаров относящиеся к 1 категории(при нажатии из меню)
def listing_products_by_category(request, catalog, category):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)

    catalog = Catalog.objects.get(slug=catalog)
    categories = Category.objects.filter(catalog=catalog.id)
    category = categories.get(slug=category)

    products = Product.objects.filter(category=category.id)
    cnt_products = len(products)
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    catalogs_categories = catalogs_categories_for_menu()

    context = {
        "catalog": catalog,
        "category": category,
        "categories": categories,
        "products": page_obj,
        "head_cat": catalogs_categories,
        "cnt_products": cnt_products,

        "cart": cart,
        "cart_count": cart_count,
        "total_price": total_price,

        "favorites": favorites,
        "fav_len": fav_len
    }

    if request.htmx:
        return render(request, 'blocks/list_products_listing_products_by_category.html', context)

    return render(request, 'shop/listing_products_by_category.html', context)


def product_detail(request, id):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)

    catalogs_categories = catalogs_categories_for_menu()

    products = Product.objects.order_by('-date_of_public')
    recommends = products[:10:] if len(products) >= 10 else products

    product = get_object_or_404(Product, id=id)

    context = {
        'head_cat': catalogs_categories,
        'product': product,
        'products': recommends,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len
    }

    return render(request, 'shop/product_detail.html', context)


# Ищем все товары относящиеся к товару, категории, катологу.
def search(request):
    cart, cart_count, total_price, favorites, fav_len = get_cart_favorites(request.user)
    catalogs_categories = catalogs_categories_for_menu()

    q = request.GET['q']

    search_from_products = Product.objects.filter(name__icontains=q)

    search_from_categories = Category.objects.filter(name__icontains=q)
    category_products = []
    if search_from_categories:
        for cat in search_from_categories:
            products = list(Product.objects.filter(category=cat.id))
            if products:
                category_products += products

    search_from_catalogs = Catalog.objects.filter(name__icontains=q)
    catalog_products = []

    if search_from_catalogs:
        for cat in search_from_catalogs:
            categories = Category.objects.filter(catalog=cat.id)
            for category in categories:
                products = list(Product.objects.filter(category=category.id))
                if products:
                    catalog_products += products

    result_products = [*search_from_products, *category_products, *catalog_products]
    paginator = Paginator(result_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'head_cat': catalogs_categories,

        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,

        'favorites': favorites,
        'fav_len': fav_len,
        # Сам параметр запроса, в случае не нахождения ни одного товара, для сообщения об этом
        'q': q
    }

    return render(request, 'shop/search.html', context)


def error_404(request, exception):
    return render(request, '404.html')