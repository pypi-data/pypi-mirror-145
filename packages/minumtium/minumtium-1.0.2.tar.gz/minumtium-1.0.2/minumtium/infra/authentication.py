from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class AuthenticationAdapter(ABC):
    """
    Adapter for an arbitrary authentication system.
    """

    def __init__(self, config: Dict, user_repo: UserRepository):
        self.initialize(config, user_repo)

    @abstractmethod
    def initialize(self, config: Dict, user_repo: UserRepository):
        ...

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """
        Validates if a given token is valid.
        :param token: the token to be validated.
        :return: True if the token is valid, else False.
        """
        ...

    @abstractmethod
    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticates an used based on its username and password.
        :param username: the username to be authenticated.
        :param password: the password to be authenticated.
        :return: the token provided for the authenticated user.
        :raises AuthenticationException: when the username and password provided are not valid.
        """
        ...

    @abstractmethod
    def encrypt_password(self, password: str) -> str:
        """
        Encrypts a password.
        :param password: the passowrd to be encrypted.
        :return: the encrypted password.
        """
        ...

    @abstractmethod
    def is_valid_password(self, password: str) -> bool:
        """
        Checks if the password provided matches the expected criteria.
        :param password: the password to be validated.
        :return: True if the password matches the criteria, else false.
        """
        ...

    @abstractmethod
    def get_password_criteria(self):
        """
        Provides a string description of the password criteria, used for error messages.
        :return: the description of the password criteria, in a human-readable way.
        """
        ...


class AuthenticationException(Exception):
    """
    Raised when there is a problem in the authentication.
    """
    ...


class AuthenticationService:
    """
    A service that interfaces with an authentication provider.
    """

    def __init__(self, adapter: AuthenticationAdapter):
        self.adapter = adapter

    def validate_token(self, token: str):
        """
        Validates if a given token is valid.
        :param token: the token to be validated.
        :raises: AuthenticationException when an invalid and/or expired token is provided.
        """
        if not self.adapter.validate_token(token):
            raise AuthenticationException('Invalid token.')

    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticates an used based on its username and password.
        :param username: the username to be authenticated.
        :param password: the password to be authenticated.
        :return: the token provided for the authenticated user.
        :raises: AuthenticationException for invalid username and/or password.
        """
        try:
            return self.adapter.authenticate(username, password)
        except Exception as e:
            raise AuthenticationException('Invalid username and/or password.') from e


from minumtium.modules.idm import UserRepository
