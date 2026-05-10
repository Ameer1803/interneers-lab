import json

from django.http import JsonResponse

from .storage import PRODUCTS, NEXT_ID


def add_product(request):
    global NEXT_ID

    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    required_fields = [
        "name",
        "description",
        "category",
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

    product_id = NEXT_ID
    NEXT_ID += 1

    product = {
        "id": product_id,
        "name": body["name"],
        "description": body["description"],
        "category": body["category"],
        "price": body["price"],
        "brand": body["brand"],
        "quantity": body["quantity"],
    }

    PRODUCTS[product_id] = product
    return JsonResponse(
        {"message": "Product created", "product": product},
        status=201,
    )


def get_product(request, product_id):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)

    product = PRODUCTS.get(product_id)
    if product is None:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse({"product": product}, status=200)


def list_product(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET allowed"}, status=405)
    
    page = int(request.GET.get("page",1))
    limit = 2

    products = list(PRODUCTS.values())
    start = (page-1)*limit
    end = start + limit

    paginated_products = products[start:end]


    return JsonResponse(
        {
            "products": paginated_products,
            "page": page
         },
        status=200,
    )


def update_product(request, product_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Only PUT allowed"}, status=405)

    product = PRODUCTS.get(product_id)

    if product is None:
        return JsonResponse({"error": "Product not found"}, status=404)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    allowed_fields = [
        "name",
        "description",
        "category",
        "price",
        "brand",
        "quantity",
    ]

    for field in allowed_fields:
        if field in body:
            product[field] = body[field]

    return JsonResponse({"product": product}, status=200)


def delete_product(request, product_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE allowed"}, status=405)

    if product_id not in PRODUCTS:
        return JsonResponse({"error": "Product not found"}, status=404)

    del PRODUCTS[product_id]

    return JsonResponse(
        {"message": "Product successfully deleted"},
        status=200,
    )