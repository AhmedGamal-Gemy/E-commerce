from configs.settings import get_settings
from core.logging import get_logger

class Base:
    def __init__(self) -> None:

        self.logger = get_logger(__name__)
        self.settings = get_settings()