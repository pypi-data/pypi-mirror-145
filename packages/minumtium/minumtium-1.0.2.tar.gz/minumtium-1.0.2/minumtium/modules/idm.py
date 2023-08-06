from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel

from minumtium.infra.database import DatabaseAdapter, DataNotFoundException

MAX_LOGIN_TRIALS = 5
LOGIN_COOLDOWN_MINUTES = 60


class User(BaseModel):
    """
    Represents an user that can be presisted in the data store.
    """
    id: str = None
    username: str
    encrypted_password: str


class Session(BaseModel):
    """
    Represents a session that can be retrieved from a JWT token.
    """
    user_id: str
    username: str
    expiration_date: datetime


class UserRepository:
    """
    Stores and retrieves user data from a data store.
    """

    def __init__(self, database_provider: DatabaseAdapter):
        self.db: DatabaseAdapter = database_provider

    def all(self) -> List[User]:
        """
        Returns a list of all users n the database.
        :return: a list of all users in the database.
        """
        try:
            return [User.parse_obj(user) for user in self.db.all()]
        except DataNotFoundException:
            return []

    def get_by_id(self, id: str) -> User:
        """
        Returns a user based on the id.
        :param id: the name of the user to look for.
        :return: an instance of the User model.
        :raises: NoUserFoundException when no user is found for the given id.
        """
        try:
            user = self.db.find_by_criteria({'id': id})[0]
            return User.parse_obj(user)
        except (IndexError, DataNotFoundException) as e:
            raise NoUserFoundException(id) from e

    def get_by_username(self, username: str) -> User:
        """
        Returns an user based on the username.
        :param username: the name of the user to look for.
        :return: an instance of the User model.
        :raises: UsernameMismatchException when more than one user has been found for this username (should not happen).
        :raises: NoUserFoundException when no user is found for the given username.
        """
        try:
            user = self.db.find_by_criteria({'username': username})
            if len(user) > 1:
                raise UsernameMismatchException(username)
            return User.parse_obj(user[0])
        except (IndexError, DataNotFoundException) as e:
            raise NoUserFoundException(username) from e

    def save(self, user: User) -> str:
        """
        Persists an user in the data store.
        :param user: an instance of User, with the username and password filled.
        :return: the id of the user inserted into the database.
        """
        return self.db.insert({'username': user.username,
                               'encrypted_password': user.encrypted_password})

    def has_user(self, username) -> bool:
        """
        Checks if a given username exists in the database.
        :param username: the name of the user to be checked.
        :return: True if the username exists, else False
        """
        try:
            self.get_by_username(username)
            return True
        except (UsernameMismatchException, NoUserFoundException):
            return False

    def delete(self, id) -> None:
        """
        Deletes an user with the id provided.
        :param id: the id of the user to be deleted.
        :raises NoUserFoundException: when an user with the id provided is not found.
        """
        try:
            self.db.delete(id)
        except DataNotFoundException:
            raise NoUserFoundException(id)


class NoUserFoundException(Exception):
    """
    Raised when an user has not been found for the username provided.
    """

    def __init__(self, username_or_id: str):
        super().__init__(f'Invalid username or id: {username_or_id}')


class UsernameMismatchException(Exception):
    """
    Raised when more than one user has been found for a given username.
    """

    def __init__(self, username: str):
        super().__init__(f'More than one username found: {username}')


class IdmService:
    """
    An identity service that provides authentication and token validation.
    """

    def __init__(self, auth_adapter: 'AuthenticationAdapter', repo: UserRepository):
        self.auth_adapter: 'AuthenticationAdapter' = auth_adapter
        self.repo: UserRepository = repo

    def is_valid_token(self, token: str) -> bool:
        """
        Checks if a given token is valid.
        :param token: the token to be validated.
        :return: True if the token is valid, else False.
        """
        return self.auth_adapter.validate_token(token)

    def authenticate(self, username: str, password: str):
        """
        Validates a username and password.
        :param username: the username to authenticate.
        :param password: the login to authenticate.
        :return: a session token to be provided back to the user.
        """
        try:
            return self.auth_adapter.authenticate(username, password)
        except Exception as e:
            raise InvalidUsernameOrPasswordException() from e

    def get_all_users_list(self) -> List[str]:
        """
        Returns a list with the name of all users in the database.
        :return: a list of usernames
        """
        users = self.repo.all()
        return [user.username for user in users]

    def put_user(self, username: str, password: str) -> bool:
        if username is None or len(username) == 0:
            raise EmptyUsernameException()

        update = self.repo.has_user(username)

        if not self.auth_adapter.is_valid_password(password):
            raise InvalidPasswordException(self.auth_adapter.get_password_criteria())

        encrypted_password = self.auth_adapter.encrypt_password(password)
        self.repo.save(User(username=username,
                            encrypted_password=encrypted_password))

        return update

    def delete_user(self, username: str) -> None:
        if username is None or len(username) == 0:
            raise EmptyUsernameException()

        try:
            user = self.repo.get_by_username(username)
            self.repo.delete(user.id)
        except NoUserFoundException as e:
            raise UserDoesNotExistException(username) from e


class UserDoesNotExistException(Exception):
    """
    Raised when trying to access an user that does not exists.
    """

    def __init__(self, username: str):
        super().__init__(f'User does not exist: {username}')


class EmptyUsernameException(Exception):
    """
    Raised when an empty username is provided.
    """

    def __init__(self):
        super().__init__('Empty usernames are not accepted.')


class InvalidPasswordException(Exception):
    """
    Raised when the password does not match the minimum criteria.
    """

    def __init__(self, criteria: str):
        super().__init__(f'The password provided does not match the minimum criteria: {criteria}')


class InvalidUsernameOrPasswordException(Exception):
    """
    Raised when an authentication error happens.
    """

    def __init__(self):
        super().__init__('Invalid username and/or password.')


from minumtium.infra.authentication import AuthenticationAdapter
