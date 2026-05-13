import requests
import pandas as pd
import streamlit as st


BASE_URL = "http://127.0.0.1:8000/products"


st.set_page_config(page_title="Products Dashboard",layout="wide")

st.title("Products Dashboard")

try:
    response = requests.get(f"{BASE_URL}/")
    data = response.json()

    products = data.get("products", [])
    try:
        category_response = requests.get(
            f"{BASE_URL}/categories/"
        )

        category_data = (
            category_response.json()
        )

        categories = category_data.get(
            "categories",
            []
        )

    except Exception:

        categories = []

except Exception as e:

    st.error(
        f"Failed to fetch products: {e}"
    )

    products = []


with st.sidebar:

    st.header("Controls")

    refresh = st.button(
        "Refresh Products"
    )

    search_term = st.text_input(
        "Search Product"
    )

    category_options = ["All"]

    category_map = {}

    for category in categories:

        category_options.append(
            category["title"]
        )

        category_map[
            category["title"]
        ] = category["id"]

    selected_category = st.selectbox(
        "Filter By Category",
        category_options
    )

if search_term:
    filtered_products = []
filtered_products = []

for product in products:

    matches_search = True

    matches_category = True

    if search_term:

        matches_search = (
            search_term.lower()
            in product["name"].lower()
        )

    if selected_category != "All":

        matches_category = (
            product["category"]["title"]
            == selected_category
        )

    if (
        matches_search
        and matches_category
    ):

        filtered_products.append(
            product
        )


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Total Products",
        len(filtered_products)
    )


with col2:

    total_quantity = sum(
        product["quantity"]
        for product in filtered_products
    )

    st.metric(
        "Total Quantity",
        total_quantity
    )


with col3:

    total_value = sum(
        product["price"] * product["quantity"]
        for product in filtered_products
    )

    st.metric(
        "Inventory Value",
        f"${total_value:.2f}"
    )


st.divider()


st.subheader("Products")


if filtered_products:

    df = pd.DataFrame(filtered_products)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.warning("No products found")


st.divider()

st.subheader("Add Product")


with st.form("add_product_form"):

    name = st.text_input("Name")

    description = st.text_input(
        "Description"
    )

    selected_form_category = (
        st.selectbox(
            "Category",
            category_options
        )
    )

    category_id = category_map.get(
        selected_form_category
    )

    brand = st.text_input("Brand")

    price = st.number_input(
        "Price",
        min_value=0.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0
    )

    submitted = st.form_submit_button(
        "Create Product"
    )


if submitted:

    payload = {
        "name": name,
        "description": description,
        "category_id": category_id,
        "price": price,
        "brand": brand,
        "quantity": quantity,
    }

    try:

        response = requests.post(
            f"{BASE_URL}/create/",
            json=payload
        )

        if response.status_code == 201:

            st.success(
                "Product created successfully"
            )

        else:

            st.error(response.text)

    except Exception as e:

        st.error(str(e))

st.divider()

st.subheader("Delete Product")


product_id = st.text_input(
    "Product ID to delete"
)


if st.button("Delete Product"):

    try:

        response = requests.delete(
            f"{BASE_URL}/{product_id}/delete/"
        )

        if response.status_code == 200:
            st.success(
                "Product deleted successfully"
            )
        else:
            st.error(response.text)
    except Exception as e:
        st.error(str(e))
