from pydantic import BaseModel

# Base dùng chung cho tạo mới và phản hồi
class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    categorie_id: int
    img: str

# Dùng khi tạo mới sản phẩm
class ProductCreate(ProductBase):
    pass

# Dùng cho phản hồi đầy đủ (ví dụ trong danh sách sản phẩm)
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductOut(Product):
    class Config:
        from_attributes = True