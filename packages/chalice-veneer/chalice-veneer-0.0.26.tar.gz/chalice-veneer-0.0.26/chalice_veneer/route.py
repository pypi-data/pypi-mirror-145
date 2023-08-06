from abc import ABC, abstractmethod
from gzip import compress
from types import GenericAlias
from typing import Dict, Iterable, List, Optional, Union

from chalice import (
    Blueprint,
    Chalice,
    CognitoUserPoolAuthorizer,
    CORSConfig,
    IAMAuthorizer,
    Response,
)
from chalice.app import MultiDict
from pydantic import BaseModel


class Route(ABC):
    class Config:
        path: str = "/"
        methods: List[str] = ["GET"]
        default_status_code: int = 200
        headers: Dict[str, str] = {}
        gzip: bool = True
        authorizer: Optional[Union[IAMAuthorizer, CognitoUserPoolAuthorizer]] = None
        inherit_authorizer: Optional[bool] = True
        cors: Optional[CORSConfig] = None
        inherit_cors: Optional[bool] = True
        catch_all_as_api_error: bool = False
        allow_multidict_query_params: bool = False

    class PathModel(BaseModel, ABC):
        ...

    class QueryModel(BaseModel, ABC):
        @classmethod
        def parse_multidict(cls, values: MultiDict) -> "Route.QueryModel":
            def _iterable_compatible(annotation) -> bool:
                """Checks if a given type annotation is compatible as an iterable"""
                if hasattr(annotation, "__origin__"):
                    if type(annotation) == GenericAlias and issubclass(
                        annotation.__origin__, Iterable
                    ):
                        return True
                    if annotation.__origin__ is Union:
                        for item in annotation.__args__:
                            if _iterable_compatible(item):
                                return True
                return False

            def _single_value_compatible(annotation) -> bool:
                """Checks if a given type annotation is compatible as a single value"""
                if hasattr(annotation, "__origin__"):
                    if annotation.__origin__ is Union:
                        for item in annotation.__args__:
                            if _single_value_compatible(item):
                                return True
                elif type(None) == annotation:
                    pass
                else:
                    return True
                return False

            result = {}
            if hasattr(cls, "__annotations__"):
                for k in values.keys():
                    value_type_def = cls.__annotations__.get(k)
                    if value_type_def:
                        value = values.getlist(k)
                        value_len = len(value)
                        if _iterable_compatible(value_type_def):
                            if (
                                _single_value_compatible(value_type_def)
                                and value_len == 1
                            ):
                                result[k] = value[0]
                            else:
                                result[k] = value
                        else:
                            result[k] = value[-1]
            return cls.parse_obj(result)

    class BodyModel(BaseModel, ABC):
        ...

    class ResponseModel(BaseModel, ABC):
        def to_response(self, headers: dict, status_code: int, gzip: bool) -> Response:
            return Response(
                body=compress(self.json().encode()) if gzip else self.json(),
                headers=headers,
                status_code=status_code,
            )

    class ApiError(Exception):
        """Base class for handling API errors"""

        class ErrorSchema(BaseModel):
            Code: str
            Message: str

        def __init__(self, message: Union[str, Exception], status_code: int):
            self.message = message if isinstance(message, str) else str(message)
            self.status_code = status_code

        def to_model(self) -> "Route.ApiError.ErrorSchema":
            return self.ErrorSchema(Code=type(self).__name__, Message=str(self.message))

        def to_response(self, headers: dict, gzip: bool) -> Response:
            return Response(
                body=compress(self.to_model().json().encode())
                if gzip
                else self.to_model().json(),
                headers=headers,
                status_code=self.status_code,
            )

    def __init__(
            self,
            app: Union[Chalice, Blueprint],
            authorizer: Optional[Union[IAMAuthorizer, CognitoUserPoolAuthorizer]] = None,
            cors: Optional[CORSConfig] = None,
    ):
        self.app = app
        chalice_kwargs = {
            "path": self.Config.path,
            "methods": [x.upper() for x in self.Config.methods],
        }

        if self.Config.inherit_authorizer:
            self.authorizer = authorizer
        else:
            self.authorizer = self.Config.authorizer
        if self.authorizer:
            chalice_kwargs["authorizer"] = self.authorizer

        if self.Config.inherit_cors:
            self.cors = cors
        else:
            self.cors = self.Config.cors
        if self.cors:
            chalice_kwargs["cors"] = self.cors

        self.app.route(**chalice_kwargs)(self._request_wrapper)

    @property
    def path_params(self) -> "Route.PathModel":
        return self.PathModel.parse_obj(self.app.current_request.uri_params or {})

    @property
    def query_params(self) -> "Route.QueryModel":
        if self.Config.allow_multidict_query_params:
            return self.QueryModel.parse_multidict(
                self.app.current_request.query_params or MultiDict(mapping={})
            )
        else:
            return self.QueryModel.parse_obj(
                self.app.current_request.query_params or {}
            )

    @property
    def body(self) -> "Route.BodyModel":
        return self.BodyModel.parse_obj(self.app.current_request.json_body or {})

    @property
    def cognito_userid(self) -> Optional[str]:
        return (
            self.app.current_request.context.get("authorizer", {})
            .get("claims", {})
            .get("sub")
        )

    @property
    def iam_user_arn(self) -> Optional[str]:
        return self.app.current_request.context.get("identity", {}).get("userArn")

    @property
    def iam_caller(self) -> Optional[str]:
        return self.app.current_request.context.get("identity", {}).get("caller")

    def _request_wrapper(self, *_, **__) -> Response:
        headers = self.Config.headers.copy()
        if self.Config.gzip:
            headers["Content-Encoding"] = "gzip"
        try:
            response = self.request()
            if isinstance(response, self.ResponseModel):
                headers["Content-Type"] = "application/json"
                return response.to_response(
                    headers, self.Config.default_status_code, self.Config.gzip
                )
            elif isinstance(response, Response):
                if not response.status_code:
                    response.status_code = self.Config.default_status_code
                response_headers = response.headers if response.headers else {}
                response.headers = {**headers, **response_headers}
                if self.Config.gzip:
                    if response.body:
                        if isinstance(response.body, str):
                            response.body = response.body.encode()
                        response.body = compress(response.body)
                return response
            else:
                raise TypeError(
                    "Return value from request must either be a Route.ResponseModel or chalice Response"
                )
        except self.ApiError as e:
            if headers.get("Content-Encoding") == "gzip":
                del headers["Content-Encoding"]
            return e.to_response(headers, gzip=False)
        except Exception as e:
            print(e)
            if self.Config.catch_all_as_api_error:
                return self.ApiError(e, 500).to_response(headers, self.Config.gzip)
            return self.ApiError("An internal server error occurred.", 500).to_response(
                headers, self.Config.gzip
            )

    @abstractmethod
    def request(self) -> Union["Route.ResponseModel", Response]:
        ...
