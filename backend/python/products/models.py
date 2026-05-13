from mongoengine import (
    Document,
    StringField,
    DecimalField,
    IntField,
    ReferenceField
)

    
class Category(Document):
    title = StringField(required=True)
    description = StringField()

class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = ReferenceField(Category)
    brand = StringField(max_length=100)

    price = DecimalField(precision=2)
    quantity = IntField(min_value=0)

    def __str__(self):
        return self.name