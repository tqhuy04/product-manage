from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from controller.send_email_controller import send_login_notification_controller

router = APIRouter()

class LoginNotificationRequest(BaseModel):
    email: EmailStr
    username: str

@router.post("/send-email", status_code=status.HTTP_200_OK)
async def send_login_email(request: LoginNotificationRequest):
    try:
        await send_login_notification_controller(
            to_email=request.email,
            username=request.username
        )
        return {"message": "Email gửi thành công"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi gửi email: {str(e)}"
        )
