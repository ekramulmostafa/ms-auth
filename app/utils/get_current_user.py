""" Get Current User """

from app.logging import Logger

logger = Logger(__name__)


def get_current_user(uuid='1000211211101'):
    logger.info("User Detail get", data={'uuid': str(uuid)})
    return uuid
