
class Config:
    MAIL_SERVER='localhost'
    MAIL_PORT=25
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False
    MAIL_DEBUG=app.debug
    MAIL_USERNAME=None
    MAIL_PASSWORD=None
    MAIL_DEFAULT_SERVER=None
    MAIL_MAX_EMAILS=None
    MAIL_SUPPRESS_SEND=app.testing
    MAIL_ASCII_ATTACHEMENTS=False