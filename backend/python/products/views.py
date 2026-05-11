import json

from django.http import JsonResponse
from products.services.product_services import ProductService
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_product(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    required_fields = [
        "name",
        "description",
        "category_id",
        "price",
        "brand",
        "quantity",
    ]

    for field in required_fields:
        if field not in body:
            return JsonResponse(
                {"error": f"Missing field: {field}"},
                status=400,
            )

    category = (CategoryService.get_category(body["category_id"]))
    body["category"] = category
    product = ProductService.create_product(body)   
    
    return JsonResponse(
        {
            "message": "Product created",
            "product": {
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "category": product.category.title,
                "price": float(product.price),
                "brand": product.brand,
                "quantity": product.quantity,
            }
        },
        status=201,
    )


def get_product(request, product_id):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    product = ProductService.get_product(prod_id=product_id)

    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse(
        {
            "product": {
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "category": product.category.title,
                "price": float(product.price),
                "brand": product.brand,
                "quantity": product.quantity,
            }
        },
        status=200,
    )


def list_product(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    
    page = int(request.GET.get("page",1))
    limit = 2

    products = ProductService.get_all_products()
    products = list(products)
    start = (page-1)*limit
    end = start + limit

    paginated_products = products[start:end]


    serialized_products = []

    for product in paginated_products:

        serialized_products.append({
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "category": product.category.title,
            "price": float(product.price),
            "brand": product.brand,
            "quantity": product.quantity,
        })

    return JsonResponse(
        {
            "products": serialized_products,
            "page": page,
        },
        status=200,
    )


def update_product(request, product_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    
    if "category_id" in body:
        category = CategoryService.get_category(body["category_id"])
    body["category"] = category
    
    product = ProductService.update_product(product_id,body)

    if product is None:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse(
        {
            "product": {
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "category": product.category.title,
                "price": float(product.price),
                "brand": product.brand,
                "quantity": product.quantity,
            }
        },
        status=200,
    )


def delete_product(request, product_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE allowed"}, status=405)

    _ = ProductService.delete_product(product_id)

    return JsonResponse(
        {"message": "Product successfully deleted"},
        status=200,
    )


@csrf_exempt
def add_category(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST allowed"},
            status=405
        )

    try:
        body = json.loads(
            request.body.decode("utf-8")
        )

    except Exception:

        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400
        )

    required_fields = [
        "title",
        "description",
    ]

    for field in required_fields:

        if field not in body:

            return JsonResponse(
                {
                    "error":
                    f"Missing field: {field}"
                },
                status=400
            )

    category = (
        CategoryService.create_category(
            body
        )
    )

    return JsonResponse(
        {
            "message": "Category created",

            "category": {
                "id": str(category.id),

                "title":
                category.title,

                "description":
                category.description,
            }
        },
        status=201,
    )


def list_category(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET allowed"},
            status=405
        )

    categories = (
        CategoryService.get_all_categories()
    )

    serialized_categories = []

    for category in categories:

        serialized_categories.append({

            "id":
            str(category.id),

            "title":
            category.title,

            "description":
            category.description,
        })

    return JsonResponse(
        {
            "categories":
            serialized_categories
        },
        status=200,
    )


def get_category(request, category_id):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET allowed"},
            status=405
        )

    category = (
        ProductCategoryService.get_category(
            category_id
        )
    )

    if not category:

        return JsonResponse(
            {"error": "Category not found"},
            status=404
        )

    return JsonResponse(
        {
            "category": {
                "id":
                str(category.id),

                "title":
                category.title,

                "description":
                category.description,
            }
        },
        status=200,
    )


@csrf_exempt
def update_category(request, category_id):

    if request.method != "PUT":
        return JsonResponse(
            {"error": "Only PUT allowed"},
            status=405
        )

    try:
        body = json.loads(
            request.body.decode("utf-8")
        )

    except Exception:

        return JsonResponse(
            {"error": "Invalid JSON body"},
            status=400
        )

    category = (
        ProductCategoryService.update_category(
            category_id,
            body
        )
    )

    if not category:

        return JsonResponse(
            {"error": "Category not found"},
            status=404
        )

    return JsonResponse(
        {
            "category": {
                "id":
                str(category.id),

                "title":
                category.title,

                "description":
                category.description,
            }
        },
        status=200,
    )


@csrf_exempt
def delete_category(request, category_id):

    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Only DELETE allowed"},
            status=405
        )

    deleted = (
        ProductCategoryService.delete_category(
            category_id
        )
    )

    if not deleted:

        return JsonResponse(
            {"error": "Category not found"},
            status=404
        )

    return JsonResponse(
        {
            "message":
            "Category successfully deleted"
        },
        status=200,
    )


# =========================================================
# CATEGORY PRODUCT APIs
# =========================================================

def get_category_products(request, category_id):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET allowed"},
            status=405
        )

    category = (
        ProductCategoryService.get_category(
            category_id
        )
    )

    if not category:

        return JsonResponse(
            {"error": "Category not found"},
            status=404
        )

    products = (
        ProductService.get_products_by_category(
            category
        )
    )

    serialized_products = []

    for product in products:

        serialized_products.append({

            "id":
            str(product.id),

            "name":
            product.name,

            "description":
            product.description,

            "price":
            float(product.price),

            "brand":
            product.brand,

            "quantity":
            product.quantity,
        })

    return JsonResponse(
        {
            "category": category.title,

            "products":
            serialized_products,
        },
        status=200,
    )


# =========================================================
# BULK CSV UPLOAD
# =========================================================

@csrf_exempt
def bulk_upload_products(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST allowed"},
            status=405
        )

    if "file" not in request.FILES:

        return JsonResponse(
            {"error": "CSV file required"},
            status=400
        )

    csv_file = request.FILES["file"]

    file_data = TextIOWrapper(
        csv_file.file,
        encoding="utf-8"
    )

    reader = csv.DictReader(file_data)

    created_products = []

    for row in reader:

        category = (
            ProductCategoryService.get_category(
                row["category_id"]
            )
        )

        if not category:
            continue

        row["category"] = category

        product = (
            ProductService.create_product(row)
        )

        created_products.append({
            "id": str(product.id),
            "name": product.name,
        })

    return JsonResponse(
        {
            "message":
            "Bulk upload completed",

            "created_products":
            created_products,
        },
        status=201,
    )