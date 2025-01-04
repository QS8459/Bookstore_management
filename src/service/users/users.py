from src.service.base import BaseService
from src.db.models.users.users import Users
from src.db.engine import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import jwt
from src.logfunc import logger

class UsersService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Users)
    def before_add(self, **kwargs):
        pass

    @staticmethod
    def encode_cookie(**kwargs):
        try:
            to_encode = kwargs.copy()
            if kwargs.get('expiration_delta'):
                expiry = datetime.utcnow() + timedelta(days = kwargs.get('expiration_delta'))
            else:
                expiry = datetime.utcnow() + timedelta(minutes = 15)
            to_encode.update({"exp": expiry})
            encode_jwt = jwt.encode(to_encode, "123", algorithm = "HS256")
            return encode_jwt
        except Exception as e:
            logger.error(f'{e}')

    @staticmethod
    def decode_cookie(**kwargs):
        try:
            decoded_cookie = jwt.decode(kwargs.get('cookie'),'123', algorithms = 'HS256' )
            logger.info(decoded_cookie)
            return decoded_cookie
        except Exception as e:
            logger.error(f'{e}')

def users_service(session:AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return UsersService(session)