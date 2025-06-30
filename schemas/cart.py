from pydantic import BaseModel
from typing import List
from schemas.product import ProductOut  # Đảm bảo đường dẫn đúng nếu không cùng thư mục

# ==== Base schema for creating/updating ====

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int
# ==== Output schemas ====

class CartItemOut(CartItemBase):
    id: int
    product: ProductOut  # Sẽ chứa thông tin sản phẩm liên quan

    class Config:
        orm_mode = True

class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut]

    class Config:
        orm_mode = True
