
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.dashboard.urls')),
    path('mei/', include('apps.mei.urls')),
    path('financas/', include('apps.finance.urls')),
    path('nfe/', include('apps.nfe.urls')),
    path('chat/', include('apps.chat.urls')),
    path('webhooks/whatsapp/', include('apps.whatsapp.urls')),
    path("", include("apps.whatsapp.urls")),
    path('das_mei/', include('apps.das_mei.urls')),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
