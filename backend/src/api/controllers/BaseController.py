from http.client import HTTPException
from core.Base import Base
from api.controllers.APIResponse import APIResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class BaseController(Base):

    def __init__(self):
        super().__init__()
    

    def build_response(self, success: bool, message: str, data=None, status_code: int = 200):
        response_model = APIResponse(success=success, message=message, data=data)
        return JSONResponse(
            content=jsonable_encoder(response_model), 
            status_code=status_code)

    async def safe_execute(self, func, *args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return self.build_response(True, "Success", result)
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error executing {func.__name__}: {e}")
            return self.build_response(False, str(e), status_code=500)
