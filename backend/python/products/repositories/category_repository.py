from products.models import Category

class CategoryRepository:
    @staticmethod
    def create(data):
        category = Category(**data)
        category.save()
        return category
    
    @staticmethod
    def get_by_id(c_id):
        category = Category.objects(id=c_id).first()
        return category
    
    @staticmethod
    def get_all():
        return Category.objects()
    
    @staticmethod
    def update(c_id,data):
        category = CategoryRepository.get_by_id(c_id)

        allowed_fields = [
            "title",
            "description",
        ]

        for field in allowed_fields:
            if field in data: setattr(category,field,data[field])
        category.save()
        return category
    
    @staticmethod
    def delete(c_id):
        category = Category.objects(id=c_id).first()
        category.delete()
        return True
    