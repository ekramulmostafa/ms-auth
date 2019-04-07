"""Role service """
# from app.models import db
from app.logging import Logger


logger = Logger(__name__)


class RoleServices:
    """Role service functions"""

    def get_current_user(self, uuid='1000211211101'):
        """ Get Current User """
        logger.info("User Detail get", data={'uuid': str(uuid)})
        return uuid
