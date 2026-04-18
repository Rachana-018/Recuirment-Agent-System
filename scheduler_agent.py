from services.email_service import send_email

async def schedule(email: str):
    link = "https://meet.google.com/demo-link"

    send_email(
        email,
        "Interview Scheduled",
        f"Join here: {link}"
    )

    return {"status": "Scheduled", "link": link}