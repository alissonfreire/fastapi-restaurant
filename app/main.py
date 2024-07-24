from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import auth
from app.schemas.response_schema import ErrorResponse

app = FastAPI()

app.include_router(auth.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    content = ErrorResponse(message='validation error', errors=exc.errors())

    return JSONResponse(status_code=422, content=content.dict())


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    match exc.status_code:
        case 401:
            content = ErrorResponse(message='unauthorized error', errors={})
        case _:
            content = ErrorResponse(message='bad request error', errors={})

    return JSONResponse(status_code=exc.status_code, content=content.dict())


@app.get('/')
def root():
    return {'hello': 'world'}
