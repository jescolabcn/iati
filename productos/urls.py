from django.urls import path
from .views import ProductoList, ProductoListCreateView, ProductoRUDView,carrito,compra

urlpatterns = [
    #path('', ProductoList.as_view(), name='producto-list'),
    path('<int:pk>', ProductoRUDView.as_view(), name='producto-retrieve-update-delete'),
    path('', ProductoListCreateView.as_view(), name='producto-list-create'),
    path('carrito', carrito, name='agregar_compra'),
    path('compra', compra, name='finalizar_compra'),
]