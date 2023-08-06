import logging

from typing import Mapping

import okta_jwt_verifier

from okta_jwt_verifier.exceptions import JWTValidationException


logger = logging.getLogger(__name__)


class OktagonException(Exception):
    pass


class InvalidTokenException(OktagonException):
    pass


class AuthorisationManager:
    def __init__(
        self,
        allowed_groups: list,
        resource_name: str,
        service_name: str,
        okta_issuer: str,
        okta_audience: str,
    ):
        self._allowed_groups = allowed_groups
        self._resource_name = resource_name
        self._service_name = service_name
        self._okta_audience = okta_audience
        self._okta_issuer = okta_issuer

    async def is_user_authorised(self, cookies: Mapping):
        try:
            access_token = cookies["access_token"]
        except KeyError:
            raise InvalidTokenException("No token provided!")

        try:
            jwt_verifier = okta_jwt_verifier.BaseJWTVerifier(issuer=self._okta_issuer, audience=self._okta_audience)
            await jwt_verifier.verify_access_token(access_token)
        except JWTValidationException as exc:
            logger.error(f"Failed to validate access token: {exc}")
            raise InvalidTokenException from JWTValidationException

        decoded_claims = jwt_verifier.parse_token(access_token)[1]

        try:
            return self.does_user_have_required_group(
                user_groups=decoded_claims["groups"],
                username=decoded_claims["sub"],
            )
        except KeyError as exc:
            raise InvalidTokenException("Groups or sub claims are not provided!") from exc

    def does_user_have_required_group(self, user_groups: list, username: str) -> bool:
        if not any(allowed_group in user_groups for allowed_group in self._allowed_groups):
            logger.warning(f"{username} is not allowed to access resource: {self._resource_name} in {self._service_name}")
            return False

        logger.info(f"{username} is allowed to access resource: {self._resource_name} in {self._service_name}")
        return True
