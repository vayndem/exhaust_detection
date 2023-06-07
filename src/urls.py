from core.api import Api
from .viewsets.index import Index
from .viewsets.knalpot import (
        exharecog
)


def init(app) -> None:
    route = Api(app, prefix='')
    route.add_resource(Index, '/')
    api = Api(app, prefix='/p')
    api.add_resource(exharecog, "/knalpot")
