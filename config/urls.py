from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from contact.views import privacy_policy

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('shop.urls')),
    path('contact/', include('contact.urls')),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
    path('privacy_policy/', privacy_policy, name='privacy_policy')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'shop.views.error_404'
