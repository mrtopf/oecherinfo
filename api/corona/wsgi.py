from corona.app import create_app
import logging

app = create_app({
    'DEBUG': False,
    'MAIL_SUPPRESS_SEND': True,  # mail will be logged to stdout
    'ENV': 'production'
})

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    pass
