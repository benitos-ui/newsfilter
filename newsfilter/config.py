from views import app
from flask_mail import Mail,Message
class Config:
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_DEBUG=app.debug
    MAIL_USERNAME='sodjine558@gmail.com'
    MAIL_PASSWORD='1234beso'
    MAIL_DEFAULT_SENDER=('service','sodjine558@gmail.com')
    MAIL_MAX_EMAILS=None
    MAIL_SUPPRESS_SEND=app.testing
    MAIL_ASCII_ATTACHEMENTS=False
mail=Mail(app)

