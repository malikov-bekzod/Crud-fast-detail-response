from fastapi import APIRouter, HTTPException, status,Depends
from schemas import OrderModel
from database.database import db
from database.models import Product, User, Order
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

order_router = APIRouter(prefix="/orders")


@order_router.post("/")
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_jwt_subject()
    except:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you're not allowed to do that")
    super_user = db.query(User).filter(User.username == claims).first()
    if super_user.is_staff:
        user = db.query(User).filter(User.id == order.user_id).first()
        product = db.query(Product).filter(Product.id == order.product_id).first()

        if user and product:
            new_order = Order(
                product_id=order.product_id,
                user_id=order.user_id,
            )
            db.add(new_order)
            db.commit()
            return HTTPException(status_code=status.HTTP_200_OK, detail="order created")
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user or product given incorrectly"
        )
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="you're not superuser so you aren't allowed to create"
    )


@order_router.get("/")
async def get_orders():
    orders = db.query(Order).all()
    context = [
        {
            "id": order.id,
            "product": {
                "id": order.products.id,
                "name": order.products.name,
                "description": order.products.description,
                "price": order.products.price
            },
            "user": {
                "id":order.users.id,
                "first_name":order.users.first_name,
                "last_name":order.users.last_name,
                "email":order.users.email,
                "username":order.users.username,
                "is_staff":order.users.is_staff
            },
            "data":{
                "status_code": 200,
            }
        }
        for order in orders
    ]
    return jsonable_encoder(context)



@order_router.get("/{id}")
async def order_detail(id:int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    new_order = {
            "id": order.id,
            "product": {
                "id": order.products.id,
                "name": order.products.name,
                "description": order.products.description,
                "price": order.products.price
            },
            "user": {
                "id":order.users.id,
                "first_name":order.users.first_name,
                "last_name":order.users.last_name,
                "email":order.users.email,
                "username":order.users.username,
                "is_staff":order.users.is_staff
            },
            "data":{
                "status_code": 200,
            }
    }
    return jsonable_encoder(new_order)


@order_router.put("/{id}")
async def update_order(id:int, order:OrderModel):
    order_check = db.query(Order).filter(Order.id == id).first()
    product_check = db.query(Product).filter(Product.id == order.product_id).first()
    user = db.query(User).filter(User.id == order.user_id).first()
    if not order_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    if not product_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
    if not user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user not found")
    for key, value in order.dict().items():
        setattr(order_check, key, value)

    db.add(order_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK,detail="updated")


@order_router.delete("/{id}")
async def delete_order(id:int):
    order_check = db.query(Order).filter(Order.id == id).first()
    if not order_check:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    db.delete(order_check)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="deleted")