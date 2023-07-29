import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
from fastapi import HTTPException
import emails
from emails.template import JinjaTemplate
from jose import jwt
import requests
from core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    print(message.charset)
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")
    if response.status_code != 250:
        raise HTTPException(status_code=400, detail="Invalid token")
        


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, username: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"Has solicitado reiniciar tu contraseña {project_name}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(athlete_id: str, email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"Te damos la bienvenida a {project_name}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html", encoding="utf-8") as f:
        template_str = f.read()
    token = generate_email_verification_token(athlete_id=athlete_id, email=email_to)
    link = f'{settings.SERVER_HOST}{settings.API_V1_STR}/auth/verify-email/{token}'
    print(link)
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
    
    
def send_confirmation_email(athlete_id: str, email_to: str, username: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"Confirma tu dirección de correo electrónico {project_name}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "resend_email_confirmation.html", encoding="utf-8") as f:
        template_str = f.read()
    token = generate_email_verification_token(athlete_id=athlete_id, email=email_to)
    link = f'{settings.SERVER_HOST}{settings.API_V1_STR}/auth/verify-email/{token}'
    print(link)
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "link": link,
        },
    )

def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.JWT_SECRET, algorithm="HS256",
    )
    return encoded_jwt


def generate_email_verification_token(athlete_id: str, email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "id": athlete_id}, settings.JWT_SECRET, algorithm="HS256",
    )
    return encoded_jwt


def verify_email_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
    
    
    

def google_get_tokens(*, code: str, redirect_uri: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data, headers=headers)

    if not response.ok:
        raise HTTPException(status_code=400, detail=f'Failed to obtain access token from Google. {response.json()}')

    tokens = {
        "access_token" : response.json()['access_token'],
        "refresh_token" : response.json()['refresh_token']
    }

    return tokens


def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        params={'access_token': access_token }
    )
    if not response.ok:
        # raise ValidationError('Failed to obtain user info from Google.')
        return response.json()

    return response.json()