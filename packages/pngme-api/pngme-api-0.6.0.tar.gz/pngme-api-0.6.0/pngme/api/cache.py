from functools import wraps
from typing import Any, Callable, Coroutine, OrderedDict, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


class Cache(OrderedDict[int, T]):
    def __init__(self, **kwargs: T) -> None:
        self.clear()
        super().__init__(**kwargs)

    def __getitem__(self, key: int) -> T:
        try:
            value = super().__getitem__(key)
            self.hits += 1
            return value
        except:
            self.misses += 1
            raise

    def __setitem__(self, key: int, value: T) -> None:
        if len(self) > 1024:
            self.popitem(False)
        super().__setitem__(key, value)

    def clear(self) -> None:
        self.hits = 0
        self.misses = 0
        super().clear()


def cache(
    function: Callable[P, Coroutine[None, None, T]]
) -> Callable[P, Coroutine[None, None, T]]:
    """Decorate function to cache return values.

    Implements a LRU cache with a default cache size of 1024 recent calls per
    function (approximately 1 MB per resource).
    """
    _cache: Cache[T] = Cache()

    @wraps(function)
    async def cached_function(*args: Any, **kwargs: Any) -> T:
        cache_key = hash(repr(args) + repr(kwargs))
        try:
            return _cache[cache_key]
        except KeyError:
            pass

        result = await function(*args, **kwargs)
        _cache[cache_key] = result
        return result

    # pylint: disable=protected-access
    cached_function._cache = _cache  # type: ignore
    return cached_function


class NotCached(Exception):
    """Raised when get_cache is passed a function that is not decorated by @cache."""


def get_cache(function: Callable[..., T]) -> Cache[T]:
    """Return the cache instance for the given function."""
    try:
        # pylint: disable=protected-access
        return function._cache  # type: ignore
    except AttributeError:
        raise NotCached("Function has not been decorated by @cache")
