from django.apps import AppConfig


class ProductsConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "products"

    def ready(self):

        import products.db  
        from products.seeds import seed_categories
        seed_categories()