from django.conf.urls import url
from .views import list_products, search_product, create_product, update_product, delete_product

urlpatterns = [
    # Ruta para listar todos los productos
    url(r'^list/$', list_products, name='list_products'),

    # Ruta para buscar un producto por su nombre
    url(r'^search/$', search_product, name='search_product'),

    # Ruta para crear un nuevo producto
    url(r'^create/$', create_product, name='create_product'),

    # Ruta para actualizar un producto existente
    url(r'^update/(?P<product_id>\d+)/$', update_product, name='update_product'),

    # Ruta para eliminar un producto existente
    url(r'^delete/(?P<product_id>\d+)/$', delete_product, name='delete_product'),
]