import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_html(
    html: str,
    subject: str,
    credentials: tuple[str, str],
    send_to: list[str] = None,
) -> None:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    username, password = credentials
    if not send_to:
        send_to = username

    email = MIMEMultipart()
    email["From"] = username
    email["To"] = send_to
    email["Subject"] = subject

    email.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(username, password)
        server.send_message(email)
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email because of '{e}'")
    finally:
        server.quit()
