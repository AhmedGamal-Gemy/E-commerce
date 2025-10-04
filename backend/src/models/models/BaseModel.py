from core.logging import get_logger

from configs.settings import get_settings


class BaseModel:

    def __init__(self, db_client : object):

        self.logger = get_logger(__name__)
        
        self.settings = get_settings()
        
        self.db_client = db_client