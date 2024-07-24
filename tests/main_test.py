from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.main import http_exception_handler, validation_exception_handler


def test_root_should_returns_ok_status(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'hello': 'world'}


@pytest.mark.asyncio
async def test_shoud_return_valid_json_format_response_for_validation_error(
    request,
):
    # arrange
    exc = RequestValidationError(errors={})
    expected_body = (
        '{"status":"fail","message":"validation error","errors":{}}'
    )

    # act
    result = await validation_exception_handler(request=request, exc=exc)
    print('result', result.body.decode('utf8'))

    # assert
    assert result.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert result.body.decode('utf8') == expected_body


@pytest.mark.asyncio
async def test_shoud_return_valid_json_format_response_for_unauthorized_error(
    request,
):
    # arrange
    exc = HTTPException(status_code=401)
    expected_body = (
        '{"status":"fail","message":"unauthorized error","errors":{}}'
    )

    # act
    result = await http_exception_handler(request=request, exc=exc)
    print('result', result.body.decode('utf8'))

    # assert
    assert result.status_code == HTTPStatus.UNAUTHORIZED
    assert result.body.decode('utf8') == expected_body


@pytest.mark.asyncio
async def test_shoud_return_json_format_bad_request_response_for_others_error(
    request,
):
    # arrange
    exc = HTTPException(status_code=400)
    expected_body = (
        '{"status":"fail","message":"bad request error","errors":{}}'
    )

    # act
    result = await http_exception_handler(request=request, exc=exc)
    print('result', result.body.decode('utf8'))

    # assert
    assert result.status_code == HTTPStatus.BAD_REQUEST
    assert result.body.decode('utf8') == expected_body
