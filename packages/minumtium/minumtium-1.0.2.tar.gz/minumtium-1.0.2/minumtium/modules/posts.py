from __future__ import annotations

from datetime import datetime
from math import ceil
from typing import Any, List

from pydantic import BaseModel

from minumtium.infra.database import DatabaseAdapter

MAX_AUTHOR_LENGTH = 64
MAX_TITLE_LENGTH = 256


class Post(BaseModel):
    """
    Represents a post that can be persisted in the data store.
    """
    id: str = None
    title: str
    author: str
    body: str = None
    timestamp: datetime = datetime.now()


class PostRepository:
    """
    Stores and retrieves post data from a data store.
    """

    def __init__(self, database_provider: DatabaseAdapter):
        self.db: DatabaseAdapter = database_provider

    def save(self, post: Post) -> str:
        """
        Stores a post into the data store.
        :param post: the instance of the Post model to be persisted.
        :return: the id of the inserted entry.
        """
        return self.db.insert(post.dict(exclude_none=True))

    def get(self, id: str) -> Post:
        """
        Retrieves a post from a data store.
        :param id: the id of the post to be retrieved.
        :return: an instance of the Post model with the data retrieved from the data store.
        :raises: PostNotFoundException in case a post has not been found for the id provided.
        """
        try:
            entry = self.db.find_by_id(id)
            return Post.parse_obj(entry)
        except Exception as e:
            raise PostNotFoundException(id) from e

    def get_all(self) -> List[Post]:
        """
        Returns all posts stored in the data store.
        :return: a list of Post instances.
        """
        return [Post.parse_obj(result) for result in self.db.all()]

    def get_for_page(self, page: int, count: int = 5) -> List[Post]:
        """
        Gets posts with pagination support.
        :param page: the page index to look posts for.
        :param count: the amount of posts to be displayed in the page.
        :return: a list of posts, with at most the count of posts provided and an offset based on the page index.
        """
        results = self.db.all(limit=count, skip=count * page)
        return [Post.parse_obj(result) for result in results]

    def get_summary(self, count: int = 10) -> List[Post]:
        """
        Returns the most recent posts in the data store.
        :param count: the amount of posts to be looked for.
        :return: a list of Post instances without body information.
        """
        results = self.db.summary(['id', 'timestamp', 'title', 'author'], limit=count)
        return [Post.parse_obj(result) for result in results]

    def count(self) -> int:
        """
        Checks how many posts there are in the data store.
        :return: the amount of posts stored in the data store.
        """
        return self.db.count()


class PostNotFoundException(Exception):
    """
    Raised when a post with a given id has not been found.
    """

    def __init__(self, post_id: str):
        super().__init__(f'Post not found: {post_id}')


class PostService:
    """
    The main service for interfacing with the Posts module.
    """

    def __init__(self, repository: PostRepository):
        self.repo: PostRepository = repository

    def get_page_count(self, page_size: int = 5) -> int:
        """
        Get the amount of post pages based on the how many posts there are in the repository.
        :param page_size: how many posts there are per page.
        :return: the count of pages.
        """
        return ceil(self.repo.count() / page_size)

    def get_posts_for_page(self, page: int, count: int = 5) -> List[Post]:
        """
        Finds all posts for a given page.
        :param page: the page to look posts for.
        :param count: how many posts there are per page.
        :return: a list of posts for a given page.
        :raises: InvalidPageArgumentException in case an invalid page is provided.
        """
        self._validate_page(page)
        self._validate_count(count)
        return self.repo.get_for_page(page, count)

    def _validate_count(self, count: int):
        if count < 0:
            raise InvalidCountArgumentException(count)

    def _validate_page(self, page: int):
        if page < 0:
            raise InvalidPageArgumentException(page)

    def get_latest_posts_summary(self, count: int = 5) -> List[Post]:
        """
        Return a list of the most recent posts.
        :param count: the amount of posts to be returned.
        :return: a list with the most recent posts added to the repository.
        """
        return self.repo.get_summary(count)

    def get_post(self, post_id: str) -> Post:
        """
        Finds a post in the repository using a given post id.
        :param post_id: the id of the post to be looked for.
        :return: an instance of Post.
        :raises: PostNotFoundException in case an invalid id is provided.
        """
        return self.repo.get(post_id)

    def add_post(self, title: str, body: str, author: str) -> str:
        """
        Saves a post into the repository.
        :param title: the title o the post.
        :param body: the body of the post.
        :param author: the author of the post.
        :return: the id of the post that has been saved.
        """
        return self.repo.save(Post(
            title=title,
            body=body,
            author=author,
            timestamp=datetime.now()))


class InvalidPageArgumentException(Exception):
    """
    Raised when an invalid page has been provided as argument.
    """

    def __init__(self, page: Any):
        super().__init__(f'Invalid page value: {str(page)}')


class InvalidCountArgumentException(Exception):
    """
    Raised when an invalid count of posts per page has been provided as argument.
    """

    def __init__(self, count: Any):
        super().__init__(f'Invalid count value: {str(count)}')
