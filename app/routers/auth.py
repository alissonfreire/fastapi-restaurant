from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.models.user import User
from app.schemas.response_schema import SuccessResponse
from app.schemas.user_schema import UserCreateInput, UserLoginInput, UserPublic
from app.services.user_service import UserService

router = APIRouter(prefix='/auth', tags=['auth'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    user_service = UserService(session=session)

    user = user_service.get_user_from_token(access_token=token)

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    return user


@router.post(
    '/register/',
    status_code=HTTPStatus.CREATED,
    response_model=SuccessResponse,
)
def register_user(
    data: UserCreateInput, session: Session = Depends(get_session)
):
    user_service = UserService(session=session)

    user, token = user_service.register_user(data=data)

    data = {'user': UserPublic(**user.__dict__), 'access_token': token}

    return SuccessResponse(data=data)


@router.post(
    '/login/',
    status_code=HTTPStatus.OK,
    response_model=SuccessResponse,
)
def login_user(data: UserLoginInput, session: Session = Depends(get_session)):
    user_service = UserService(session=session)

    result = user_service.login_user(data=data)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    user, token = result

    data = {'user': UserPublic(**user.__dict__), 'access_token': token}

    return SuccessResponse(data=data)


@router.get(
    '/me/',
    status_code=HTTPStatus.OK,
    response_model=SuccessResponse,
)
def me(user: User = Depends(get_current_user)):
    return SuccessResponse(data={'user': UserPublic(**user.__dict__)})
