from mongoengine import connect

connect(
    db="products_db",
    host="mongodb://root:example@localhost:27019/products_db?authSource=admin"
)