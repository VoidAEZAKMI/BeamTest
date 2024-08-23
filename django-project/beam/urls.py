from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('api/', include(router.urls)),
    path('swagger/', views.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
