from typing import List, Optional, Type, Union

from chalice import Blueprint, CognitoUserPoolAuthorizer, CORSConfig, IAMAuthorizer

from .route import Route


class ServiceBlueprint:
    def __init__(
        self,
        routes: Optional[List[Type[Route]]] = None,
        sub_blueprints: Optional[List["ServiceBlueprint"]] = None,
        url_prefix: Optional[str] = "/",
        import_name: Optional[str] = None,
        extend_parent_prefix: Optional[bool] = True,
        authorizer: Optional[Union[CognitoUserPoolAuthorizer, IAMAuthorizer]] = None,
        inherit_authorizer: Optional[bool] = True,
        cors: Optional[CORSConfig] = None,
        inherit_cors: Optional[bool] = True,
    ):
        self.import_name = import_name or __name__
        self.blueprint = Blueprint(self.import_name)
        self.routes = routes or []
        self._instantiated_routes = []
        self.sub_blueprints = sub_blueprints or []
        self.url_prefix = url_prefix
        self.extend_parent_prefix = extend_parent_prefix
        self.authorizer = authorizer
        self.inherit_authorizer = inherit_authorizer
        self.cors = cors
        self.inherit_cors = inherit_cors
        self._registered = False

    def propagate(
        self,
        authorizer: Optional[Union[CognitoUserPoolAuthorizer, IAMAuthorizer]] = None,
        cors: Optional[CORSConfig] = None,
    ):
        if self._registered:
            # If attempting to register a blueprint again through another blueprint, make new blueprint object
            self.blueprint = Blueprint(self.import_name)
            # Instantiated routes can only be appended to, so on re-registering, reset so no old routes are added
            self._instantiated_routes = []

        if self.inherit_authorizer:
            self.authorizer = authorizer
        if self.inherit_cors:
            self.cors = cors
        for route in self.routes:
            self._instantiated_routes.append(route(self.blueprint, self.authorizer, self.cors))
        self._registered = True
