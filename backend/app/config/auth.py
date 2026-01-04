from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Optional

from fastapi import HTTPException, Request, status

__all__ = ["enable_auth"]


def enable_auth(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request = _extract_request(args, kwargs)
        if request is None:
            raise RuntimeError("auth decorator requires a FastAPI Request argument.")

        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Authorization header",
            )

        result = func(*args, **kwargs)
        if inspect.isawaitable(result):
            return await result
        return result

    return wrapper


def _extract_request(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Optional[Request]:
    request = kwargs.get("request")
    if isinstance(request, Request):
        return request

    for arg in args:
        if isinstance(arg, Request):
            return arg

    return None


def get_user(request: Request) -> str:
    return str(request.headers.get("Authorization")).split(" ")[-1]
