from quart import Quart, Blueprint, request, abort, g, Response

from inspect import isasyncgen, isgenerator
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response as WerkzeugResponse
from werkzeug.datastructures import Headers
from quart.wrappers import Response
from quart.typing import (
    ResponseReturnValue,
    ResponseTypes,
    HeadersValue,
    StatusCode,
)

from .dictify import dictify

from utils.logger import logger
class XQuart(Quart):
    '''
    Copied from https://github.com/pallets/quart/blob/main/src/quart/app.py#L1341
    Changed at MAIN CHANGE
    '''

    async def make_response(self, result: ResponseReturnValue | HTTPException) -> ResponseTypes:
        headers: HeadersValue | None = None
        status: StatusCode | None = None

        # logger.debug(f"Result: {result}")
        if isinstance(result, tuple):
            if len(result) == 3:
                value, status, headers = result
            elif len(result) == 2:
                value, status_or_headers = result

                if isinstance(status_or_headers, (Headers, dict, list)):
                    headers = status_or_headers
                    status = None
                elif status_or_headers is not None:
                    status = status_or_headers  # type: ignore[assignment]
            else:
                raise TypeError(
                    """The response value returned must be either (body, status), (body,
                    headers), or (body, status, headers)"""
                )
        else:
            value = result  # type: ignore[assignment]

        if value is None:
            raise TypeError("The response value returned by the view function cannot be None")

        response: ResponseTypes
        if isinstance(value, HTTPException):
            response = value.get_response()  # type: ignore
        elif not isinstance(value, (Response, WerkzeugResponse)):
            if (
                isinstance(value, (str, bytes, bytearray))
                or isgenerator(value)
                or isasyncgen(value)
            ):
                response = self.response_class(value)
            # MAIN CHANGE
            # elif isinstance(value, (list, dict)):
            elif not isinstance(value, Exception):
                d = dictify(value)
                response = self.json.response(d)  # type: ignore[assignment]
            else:
                raise TypeError(f"The response value type ({type(value).__name__}) is not valid")
        else:
            response = value

        if status is not None:
            response.status_code = int(status)

        if headers is not None:
            response.headers.update(headers)  # type: ignore[arg-type]

        return response

