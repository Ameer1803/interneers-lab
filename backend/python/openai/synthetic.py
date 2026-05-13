import os,json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel,ValidationError
from mongoengine import connect,Document,StringField,FloatField,IntField

load_dotenv()

client=OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

connect(
    db="products_db",
    host="mongodb://root:example@localhost:27019/products_db?authSource=admin"
)

class Product(Document):
    name=StringField(required=True)
    description=StringField()
    brand=StringField(required=True)
    price=FloatField(required=True)
    quantity=IntField(required=True)
    category=StringField()

class ProductSchema(BaseModel):
    name:str
    description:str
    brand:str
    price:float
    quantity:int
    category:str

# response=client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[{
#         "role":"user",
#         "content":"Generate 5 product names for a toy store"
#     }],
#     temperature=0.7
# )

# print("\nRAW RESPONSE:\n")
# print(response.choices[0].message.content)

# print("\nTOKEN USAGE:\n")
# print(response.usage)

# for temp in [0.0,0.7,1.5]:

#     print(f"\nTEMPERATURE={temp}\n")

#     response=client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{
#             "role":"user",
#             "content":"Generate 5 product names for a toy store"
#         }],
#         temperature=temp
#     )

#     print(response.choices[0].message.content)

prompt="""
Generate 50 toy store products.
Return ONLY a valid JSON array.

Each object must contain:
- name
- description
- brand
- price
- quantity
- category
"""

response=client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{
        "role":"user",
        "content":prompt
    }],
    temperature=0.8
)

raw_output=response.choices[0].message.content

print("\nRAW JSON OUTPUT:\n")
print(raw_output)
cleaned = raw_output.replace("```","").strip()
try:
    products=json.loads(cleaned)
    print("\nJSON parsing successful")
except Exception as e:
    print("\nJSON parsing failed")
    print(e)
    products=[]

validated_products=[]

for product in products:

    try:
        validated=ProductSchema(**product)
        validated_products.append(validated)
        print(f"Validated: {validated.name}")

    except ValidationError as e:
        print("\nValidation failed:\n")
        print(e)

print(f"\nTOTAL VALID PRODUCTS: {len(validated_products)}")

for product in validated_products:

    mongo_product=Product(
        name=product.name,
        description=product.description,
        brand=product.brand,
        price=product.price,
        quantity=product.quantity,
        category=product.category
    )

    mongo_product.save()

    print(f"Saved: {product.name}")

print("\nDATABASE INSERT COMPLETE")