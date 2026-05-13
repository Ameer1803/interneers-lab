from products.repositories.category_repository import CategoryRepository

class CategoryService:
    @staticmethod
    def create_category(data):
        return CategoryRepository.create( data)

    @staticmethod
    def get_category(prod_id):
        return CategoryRepository.get_by_id(prod_id)

    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def delete_category(prod_id):
        return CategoryRepository.delete(prod_id)