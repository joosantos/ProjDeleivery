from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, UUID4
from typing import List
from schemas import Team, Competition
from datetime import datetime

from .environment import config

MAIL_USERNAME = config.get("mail.username", "5de1a39925cc98")
MAIL_PASSWORD = config.get("mail.password", "1d6bdf080ea269")
MAIL_FROM = config.get("mail.from", "")
MAIL_FROM_NAME = config.get("mail.from_name", "")
MAIL_PORT = config.get("mail.port", "2525")
MAIL_SERVER = config.get("mail.server", "smtp.mailtrap.io")
MAIL_SSL_TLS = config.get("mail.ssl_tls") == "True"
MAIL_STARTTLS = config.get("mail.starttls") == "True"
ADMIN_MAIL = config.get("mail.admin_mail", "competicao.kempo@gmail.com")
CONTABILITY_EMAIL = config.get("mail.contability_email", "competicao.kempo@gmail.com")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_FROM=MAIL_FROM,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    MAIL_STARTTLS=MAIL_STARTTLS,
)


async def send_blocked_coach(recipient: EmailStr):
    content: str = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Blocked!</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            Your account was blocked by our administrators. If you believe this is an error please contact us at <a herf=\"mailto:geral@fplk-kempoportugal.com\">geral@fplk-kempoportugal.com</a>.
        </p>
    </body>
</html>
"""
    return await send_mail(recipients=[recipient], body=content, subject="Blocked!")


async def send_unblocked_coach(recipient: EmailStr):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Unblocked!</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            Your account was unblocked by our administrators! You can now login as normal.
        </p>
        <br />
        <a href=\"{config.get("app.url")}login\">
            Login
        </a>
    </body>
</html>
"""
    return await send_mail(recipients=[recipient], body=content, subject="Unblocked!")


async def send_verified_coach(recipient: EmailStr):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Verified!</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            Your account was verified by our administrators! You can now login to start creating your team(s).
        </p>
        <br />
        <a href=\"{config.get("app.url")}login\">
            Login
        </a>
    </body>
</html>
"""
    return await send_mail(recipients=[recipient], body=content, subject="Verified!")


async def send_not_verified_coach(recipient: EmailStr):
    content: str = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Account Refused</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            Your account was refused by our administrators. If you believe this is an error please contact us at <a herf=\"mailto:geral@fplk-kempoportugal.com\">geral@fplk-kempoportugal.com</a>.
        </p>
    </body>
</html>
"""
    return await send_mail(
        recipients=[recipient], body=content, subject="Account Refused"
    )


async def send_verify_admin():
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>New User To Verify</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            There is a new coach awaiting you to verify their new account!
        </p>
        <br />
        <a href=\"{config.get("app.url")}admin/verify-coaches\">
            Verify Coach
        </a>
    </body>
</html>
"""
    return await send_mail(
        recipients=[ADMIN_MAIL], body=content, subject="New User To Verify"
    )


async def send_new_payment_comprovative(file_name: str, team: Team):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>New payment comprovative uploaded</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            The team {team.name} ({team.abbreviation}) has uploaded a new payment comprovative
        </p>
        <br />
        <a href=\"{config.get("app.api")}insurances/get-payment-guide?payment_comprovative={file_name}\">
            See Payment Guide
        </a>
        <br />
        <a href=\"{config.get("app.file_storage")}{file_name}\">
            See Payment Comprovative
        </a>
        <br />
        <a href=\"{config.get("app.url")}admin/insurances?page=0&year={datetime.today().year}&teamabbreviation={team.abbreviation}&groupby=payment_comprovatives\">
            See Insurance Group
        </a>
        <br />
        <a href=\"{config.get("app.url")}admin/insurances/group?paymentcomprovativeurl={file_name}&insurancegroup=\">
            See Insurance Group Details
        </a>
    </body>
</html>
"""
    return await send_mail(
        recipients=[CONTABILITY_EMAIL],
        body=content,
        subject="New Payment Comprovative Uploaded",
    )


async def send_new_payment_comprovative_for_inscriptions(
    file_name: str, team: Team, competition: Competition
):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>New payment comprovative uploaded</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            The team {team.name} ({team.abbreviation}) has uploaded a new payment comprovative
        </p>
        <br />
        <a href=\"{config.get("app.api")}inscriptions/get-payment-guide?payment_comprovative={file_name}&team_id={team.id}\">
            See Payment Guide
        </a>
        <br />
        <a href=\"{config.get("app.file_storage")}{file_name}\">
            See Payment Comprovative
        </a>
        <br />
        <a href=\"{config.get("app.url")}competition/{competition.id}/inscriptions/team/{team.id}\">
            See Team Inscriptions
        </a>
        <br />
    </body>
</html>
"""
    return await send_mail(
        recipients=[CONTABILITY_EMAIL],
        body=content,
        subject=f"New Payment Comprovative For {competition.name}",
    )


async def send_unauthorized_email(root: bool, docs: bool, redocs: bool, host):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Unauthorized access</title>
    </head>
    <body style="font-size: 1rem">
        {'<p>Someone accessed to the root url</p>' if root else ''}
        {'<p>Someone accessed to the docs url</p>' if docs else ''}
        {'<p>Someone accessed to the redocs url</p>' if redocs else ''}
        <p>Host: {host}</p>
        <br />
    </body>
</html>
"""
    return await send_mail(
        recipients=["miguelangeloleal@hotmail.com"],
        body=content,
        subject="Unauthorized access",
    )


async def send_register_confirmation(recipient: EmailStr, id: UUID4):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>Email Confirmation</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            Thank you for registering in our website, please click the following link to confirm your email to finish your registration
        </p>
        <br />
        <a href="{config.get("app.url")}auth/confirm/{str(id)}">
            Confirm Registration
        </a>
    </body>
</html>
"""
    return await send_mail(
        recipients=[recipient], body=content, subject="Email Confirmation"
    )


async def send_mail(recipients: List[EmailStr], body: str, subject: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        subtype=MessageType.html,
        body=body,
    )

    fast_email = FastMail(conf)
    await fast_email.send_message(message)
    return


async def send_inscriptions_information(
    competition_name: str, team_name: str, coach_name: str, number_inscriptions: int
):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>New Inscriptions for {competition_name}</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            The coach {coach_name} of the team {team_name} has submitted {number_inscriptions} new inscriptions for the competition {competition_name}
        </p>
    </body>
</html>
"""
    return await send_mail(
        recipients=[ADMIN_MAIL],
        body=content,
        subject=f"New Inscriptions for {competition_name}",
    )


async def send_federation_requests_to_admin(
    name: str, number_federations: int, team_name: str
):
    content: str = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>New Federation Requests for {team_name} ({number_federations})</title>
    </head>
    <body style="font-size: 1rem">
        <p>
            The coach {name} of the team {team_name} has submitted {number_federations} new federation requests.
        </p>
        <a href=\"{config.get("app.url")}admin/\">
            See federation requests
        </a>
    </body>
</html>
"""
    return await send_mail(
        recipients=[ADMIN_MAIL],
        body=content,
        subject=f"New Inscriptions for {competition_name}",
    )
