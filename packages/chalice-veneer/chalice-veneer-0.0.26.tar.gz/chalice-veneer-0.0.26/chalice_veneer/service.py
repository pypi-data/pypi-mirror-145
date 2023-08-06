from typing import List, Optional, Type, Union

from chalice import Chalice, CognitoUserPoolAuthorizer, CORSConfig, IAMAuthorizer

from .route import Route
from .service_blueprint import ServiceBlueprint


class Service:
    def __init__(
        self,
        app: Chalice,
        routes: Optional[List[Type[Route]]] = None,
        binary_types: Optional[List[str]] = None,
        authorizer: Optional[Union[CognitoUserPoolAuthorizer, IAMAuthorizer]] = None,
        cors: Optional[CORSConfig] = None,
    ):
        self.app = app
        if binary_types:
            self.app.api.binary_types.extend(binary_types)
        self.routes = routes or []
        self._instantiated_routes = []
        self.authorizer = authorizer
        self.cors = cors
        for route in self.routes:
            self._prepare_route(route)
        self.blueprints: List[ServiceBlueprint] = []

    def register_service_blueprint(
        self,
        service_blueprint: ServiceBlueprint,
        parent_prefix: Optional[str] = None,
        parent_service_blueprint: Optional["ServiceBlueprint"] = None,
    ):
        if not parent_service_blueprint:
            self.blueprints.append(service_blueprint)
        service_blueprint.propagate(
            parent_service_blueprint.authorizer
            if parent_service_blueprint
            else self.authorizer,
            parent_service_blueprint.cors if parent_service_blueprint else self.cors,
        )
        if service_blueprint.extend_parent_prefix and parent_prefix:
            if parent_prefix.endswith("/"):
                prefix = parent_prefix[:-1]
            else:
                prefix = parent_prefix
            prefix = f"{prefix}{service_blueprint.url_prefix}"
        else:
            prefix = service_blueprint.url_prefix

        self.app.register_blueprint(service_blueprint.blueprint, url_prefix=prefix)
        for blueprint in service_blueprint.sub_blueprints:
            self.register_service_blueprint(blueprint, prefix, service_blueprint)

    def _prepare_route(self, route: Type[Route]):
        self._instantiated_routes.append(route(self.app, self.authorizer, self.cors))

    def register_routes(self, routes: Union[Type[Route], List[Type[Route]]]):
        if type(routes) == Route:
            self.routes.append(routes)
            self._prepare_route(routes)
        else:
            self.routes.extend(routes)
            for route in routes:
                self._prepare_route(route)
