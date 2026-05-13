from django.urls import path
from .views import (
    add_product,
    get_product,
    list_product,
    update_product,
    delete_product,
)
from .views import (
    add_category,
    get_category,
    list_category,
    update_category,
    delete_category,
    get_category_products,
)
urlpatterns = [
    path("", list_product),
    path("create/", add_product),
    path("categories/", list_category),
    path("categories/create/", add_category),
    path("categories/<str:category_id>/",get_category),
    path("categories/<str:category_id>/update/",update_category),
    path("categories/<str:category_id>/delete/",delete_category),
    path("categories/<str:category_id>/products/",get_category_products),
    path("<str:product_id>/", get_product),
    path("<str:product_id>/update/", update_product),
    path("<str:product_id>/delete/", delete_product),
]