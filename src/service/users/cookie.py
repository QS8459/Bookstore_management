from sqlalchemy.ext.asyncio import AsyncSession
from src.service.base import BaseService
from src.db.engine import get_async_session
from src.db.models.users.cookie import Cookie
from fastapi import Depends

class CookieService(BaseService):
    def __init__(self, session):
        super().__init__(session, Cookie)

    def before_add(self, **kwargs):
        pass

    def _hash_ip(self, ip: str):
        """
                Hashes the given IP address using SHA-256.

                :param ip: The IP address to hash.
                :return: A hashed version of the IP address.
                :raises ValueError: If hashing fails.
        """
        try:
            pass
            # return sha256.hash(ip)
        except Exception as e:
            raise ValueError(f"Failed to hash IP {e}")
    def hash_and_add_ip(self, ip: str):
        hashed_ip = self._hash_ip(ip)
        self.add(value = hashed_ip)

def cookie_service(session: AsyncSession = Depends(get_async_session)) -> CookieService:
    return CookieService(session)