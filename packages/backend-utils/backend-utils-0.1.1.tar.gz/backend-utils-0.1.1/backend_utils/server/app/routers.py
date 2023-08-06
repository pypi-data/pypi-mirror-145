from dataclasses import dataclass
from typing import List

from fastapi import APIRouter, FastAPI


def _prefix_validation_error(name: str):
    return ValueError(f'{name} must start with /')


@dataclass
class Router:
    """
    Router class to wrap fastapi.APIRouter

    router: fastapi APIRouter
    tags: to compile router endpoints in openapi scheme
    prefix: prefix for all endpoints in router
    """

    router: APIRouter
    tags: List[str] = None
    prefix: str = ''

    def __setattr__(self, name, value):
        """Validate Router fields"""

        if name == 'prefix':
            if not value.startswith('/'):
                raise _prefix_validation_error(name='prefix')
        self.__dict__[name] = value


def compile_routers(routers: List[Router], root_prefix: str = ''):
    """Enrich routers with root_prefix for every endpoint in routers"""

    if root_prefix and not root_prefix.startswith('/'):
        raise _prefix_validation_error(name='root_prefix')

    for router in routers:
        router.prefix = root_prefix + router.prefix

    return routers


def register_routers(app: FastAPI, routers: List[Router]):
    """Add routers to fastapi app"""

    for router in routers:
        app.include_router(
            router=router.router,
            tags=router.tags,
            prefix=router.prefix
        )
