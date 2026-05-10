from django.urls import path
from .views import (
    add_product,
    get_product,
    list_product,
    update_product,
    delete_product,
)

urlpatterns = [
    path("products/", list_product),
    path("products/create/", add_product),
    path("products/<int:product_id>/", get_product),
    path("products/<int:product_id>/update/", update_product),
    path("products/<int:product_id>/delete/", delete_product),
]