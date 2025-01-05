from fastapi import Depends, APIRouter, Response, Request
from src.service.users.users import users_service
from src.service.users.cookie import cookie_service
from src.schema.users.users import UserSchema
from src.logfunc import logger
users_api = APIRouter(prefix="/user")

@users_api.post('/visit', status_code = 200)
async def visit(
    response: Response,
    request: Request,
    service = Depends(users_service),
    service_co = Depends(cookie_service)
):
    # Front end needs to send "Authorization" in headers so backend would be able to distingush them
    check_ip = await service.filter(ip_address = f"{request.client.host}")
    logger.info(f"Check ip value: {check_ip}")
    if check_ip is None:

        user = await service.add(ip_address = f"{request.client.host}")
        # id, cookie_id if you want you may also give expiration_delta in days
        user_info = UserSchema(id = str(user.id), ip_address = user.ip_address)

        encoded_cookie = service.encode_cookie(**user_info.dict())

        # Service, cookie encoder
        encoded_response = await service_co.add(value = encoded_cookie, refresh_value = '')

        user_updated = await service.update(id = user.id,cookie_id = encoded_response.id)

        response.headers.update({'Set-Cookie':encoded_cookie})
        return "OK"
    else:
        return "Already Authorized"


@users_api.get('/me', status_code = 200)
async def me(
        request: Request,
        service = Depends(users_service)
):
    cookie = request.headers.get('Cookie')
    logger.info(request.client.host)
    decoded_cookie = service.decode_cookie(cookie = cookie)
    # logger.info(f"Me cookie {decoded_cookie}")
    return "OK"