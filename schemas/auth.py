from pydantic import BaseModel
from typing import Optional

# Base thông tin người dùng
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

# Schema để tạo user - cho phép truyền role (mặc định là "user")
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "user"  # 👈 Thêm dòng này

# Schema đăng nhập
class UserLogin(BaseModel):
    username: str
    password: str

# Schema trả về sau khi tạo hoặc truy xuất user
class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

# Schema token phản hồi khi đăng nhập
class Token(BaseModel):
    access_token: str
    token_type: str
