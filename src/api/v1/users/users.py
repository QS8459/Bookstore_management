from fastapi import Depends, APIRouter, Response, Request
from src.service.users.users import users_service
from src.schema.users.users import UserSchema
from src.logfunc import logger
users_api = APIRouter(prefix="/user")

@users_api.post('/visit', status_code = 200)
async def visit(
    response: Response,
    request: Request,
    service = Depends(users_service)
):
    #Front end needs to send "Authorization" in headers so backend would be able to distingush them
    if service.cookie_auth(request.headers.get('Authorization')):
        user = await service.add()
    #id, cookie_id if you want you may also give expiration_delta in days
        user_info = UserSchema(id = str(user.id), cookie_id = str(user.cookie_id))

    #Service, cookie encoder
        encoded_cookie = service.encode_cookie(**user_info.dict())
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