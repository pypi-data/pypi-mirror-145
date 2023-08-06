from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.conflict_error import ConflictError
from ...models.forbidden_error import ForbiddenError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    app_id: str,
) -> Dict[str, Any]:
    url = "{}/apps/{app_id}/manifest.yaml".format(client.base_url, app_id=app_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[BadRequestError, ForbiddenError, ConflictError]]:
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json())

        return response_403
    if response.status_code == 409:
        response_409 = ConflictError.from_dict(response.json())

        return response_409
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[BadRequestError, ForbiddenError, ConflictError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    app_id: str,
) -> Response[Union[BadRequestError, ForbiddenError, ConflictError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    app_id: str,
) -> Optional[Union[BadRequestError, ForbiddenError, ConflictError]]:
    """ Create or update from an app manifest """

    return sync_detailed(
        client=client,
        app_id=app_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    app_id: str,
) -> Response[Union[BadRequestError, ForbiddenError, ConflictError]]:
    kwargs = _get_kwargs(
        client=client,
        app_id=app_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    app_id: str,
) -> Optional[Union[BadRequestError, ForbiddenError, ConflictError]]:
    """ Create or update from an app manifest """

    return (
        await asyncio_detailed(
            client=client,
            app_id=app_id,
        )
    ).parsed
