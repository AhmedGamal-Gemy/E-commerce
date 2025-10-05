from configs.settings import get_settings
from core.logging import get_logger
from core.Base import Base

class BaseService(Base):

    def __init__(self):
        super().__init__()


    async def safe_execute(self, func, *args, **kwargs):
        """Executes a function safely and logs exceptions."""
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing {func.__name__}: {str(e)}")
            raise e
