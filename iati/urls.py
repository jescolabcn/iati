from django.urls import include, re_path,path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Gorras&Kmisetas",
        default_version='v1.0',
        description="API para gestionar productos y carrito de compras.",
        terms_of_service="https://www.gorrasKmisetas.com",
        contact=openapi.Contact(email="contact@gorrasKmisetas.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^productos/', include(('productos.urls','productos'),namespace="productos")),        
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]


