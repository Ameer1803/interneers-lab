from products.models import ProductCategory


DEFAULT_CATEGORIES = [

    {
        "title": "Food",
        "description": "Groceries and snacks",
    },

    {
        "title": "Kitchen Essentials",
        "description": "Kitchen products",
    },

    {
        "title": "Electronics",
        "description": "Electronic gadgets",
    },

    {
        "title": "Books",
        "description": "Books and stationery",
    },
]


def seed_categories():

    for category_data in DEFAULT_CATEGORIES:

        existing_category = (
            ProductCategory.objects(
                title=category_data["title"]
            ).first()
        )

        if not existing_category:

            ProductCategory(
                **category_data
            ).save()

            print(
                f"Created category: "
                f"{category_data['title']}"
            )

        else:

            print(
                f"Category already exists: "
                f"{category_data['title']}"
            )