from fastapi import APIRouter, HTTPException, status
from schemas import ProductModel
from database.database import db
from database.models import Product, Category
from fastapi.encoders import jsonable_encoder

product_router = APIRouter(prefix="/products")


@product_router.post("/")
async def create_product(product: ProductModel):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if category:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id,
        )
        db.add(new_product)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="product created")
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating a product"
    )


@product_router.get("/")
async def get_products():
    products = db.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "category": {
                "id":product.category.id,
                "name":product.category.name,
            },
            "data":{
                "status_code": 200,
            }
        }
        for product in products
    ]
    return jsonable_encoder(context)



@product_router.get("/{id}")
async def product_detail(id:int):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    new = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
            "category": {
                "id":product.category.id,
                "name":product.category.name,
            },
            "data":{
                "status_code": 200,
            }
        }
    return jsonable_encoder(product)


@product_router.put("/{id}")
async def update_product(id:int, product:ProductModel):
    product_check = db.query(Product).filter(Product.id == id).first()
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not product_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
    if not category:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="category not found")

    for key, value in product.dict().items():
        setattr(product_check, key, value)

    db.add(product_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK,detail="updated")


@product_router.delete("/{id}")
async def delete_product(id:int):
    product_check = db.query(Product).filter(Product.id == id).first()
    if not product_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    db.delete(product_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="deleted")