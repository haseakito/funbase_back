from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from schemas.user import EmailSchema
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '../.env')
# Load the environment variables
load_dotenv(env_path)

# FastMail config
configs = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER='./templates/'
)

"""
Asynchronous function handling sending email
"""
async def send_email(data: EmailSchema):

    # message schema
    message = MessageSchema(
        subject='Funbase',
        recipients=data.dict().get('email'),
        template_body=data.dict().get('body'),
        subtype=MessageType.html
    )

    fm = FastMail(configs)

    await fm.send_message(message, template_name='email.html')