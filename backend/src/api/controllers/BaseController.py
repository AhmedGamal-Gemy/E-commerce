from http.client import HTTPException
from core.Base import Base
from api.controllers.APIResponse import APIResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class BaseController(Base):

    def __init__(self):
        super().__init__()
    