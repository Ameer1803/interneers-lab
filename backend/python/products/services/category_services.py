from products.repositories.product_repository import ProductRepository

class CategoryService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create( data)

    @staticmethod
    def get_product(prod_id):
        return ProductRepository.get_by_id(prod_id)

    @staticmethod
    def get_all_products():
        return ProductRepository.get_all()

    @staticmethod
    def delete_product(prod_id):
        return ProductRepository.delete(prod_id)