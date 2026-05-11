from products.models import Product

class ProductRepository:
    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product
    
    @staticmethod
    def get_by_id(prod_id):
        product = Product.objects(id=prod_id).first()
        return product
    
    @staticmethod
    def get_all():
        return Product.objects()
    
    @staticmethod
    def update(prod_id,data):
        product = ProductRepository.get_by_id(prod_id)

        allowed_fields = [
            "name",
            "description",
            "category",
            "price",
            "brand",
            "quantity",
        ]

        for field in allowed_fields:
            if field in data: setattr(product,field,data[field])
        product.save()
        return product
    
    @staticmethod
    def delete(prod_id):
        product = Product.objects(id=prod_id).first()
        product.delete()
        return True
    