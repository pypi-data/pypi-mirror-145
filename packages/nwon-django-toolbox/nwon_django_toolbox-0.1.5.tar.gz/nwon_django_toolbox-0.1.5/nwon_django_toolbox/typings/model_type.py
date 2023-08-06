from typing import Generic, Iterator, TypeVar, Union

from django.db.models import QuerySet

T = TypeVar("T")


class ModelType(Generic[T]):
    def __iter__(self) -> Iterator[Union[T, QuerySet]]:
        pass


__all__ = ["ModelType"]
