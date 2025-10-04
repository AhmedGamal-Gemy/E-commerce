from BaseModel import BaseModel
from models.schemas.user import User

class UserModel(BaseModel):

    def __init__(self, db_client: object):

        super().__init__( db_client = db_client )

        self.logger.info(f"UserModel initialized")

    # EXAMPLE METHODS - Uncomment and implement as needed

    # async def get_user_by_id(self, user_id: int) -> User:
    #     pass

    # async def create_user(self, user: User) -> int:
    #     pass

    # async def update_user(self, old_user: User, new_user: User) -> User:
    #     pass

    # async def delete_user(self, user: User) -> int:
    #     pass