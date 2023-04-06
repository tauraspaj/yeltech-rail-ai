from common import logger

from app import flask

app = flask.create_app()
log = logger.setup_logger()

if __name__ == "__main__":
    log.info("Starting API...")
    app.run()
