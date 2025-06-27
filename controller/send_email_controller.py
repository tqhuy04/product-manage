from util.email import send_login_notification

async def send_login_notification_controller(to_email: str, username: str):
    await send_login_notification(to_email=to_email, username=username)
