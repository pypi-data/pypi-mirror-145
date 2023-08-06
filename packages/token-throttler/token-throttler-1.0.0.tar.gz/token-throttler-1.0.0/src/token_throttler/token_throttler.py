import asyncio
from inspect import formatannotation, signature
from typing import Any, Callable

from . import TokenBucket, TokenThrottlerException
from .storage import BucketStorage


class TokenThrottler:
    def __init__(self, cost: int, storage: BucketStorage) -> None:
        self._cost: int = cost
        self._buckets: BucketStorage = storage
        self._validate_init()

    def _validate_init(self) -> None:
        if not isinstance(self._cost, int):
            raise TypeError("Invalid `cost` type")
        if not isinstance(self._buckets, BucketStorage):
            raise TypeError("Invalid `storage` class")

    @staticmethod
    def _validate_identifier(identifier: str) -> None:
        if not isinstance(identifier, str):
            raise TypeError("Invalid `identifier` type")

    @staticmethod
    def _validate_add_bucket(bucket: TokenBucket) -> None:
        if not isinstance(bucket, TokenBucket):
            raise TypeError("Invalid `bucket` type")

    @staticmethod
    def _validate_add_from_dict(bucket_config: list[dict[str, Any]]) -> None:
        token_bucket_params: dict = {
            p.name: p.annotation for p in signature(TokenBucket).parameters.values()
        }
        if not all(
            key in bucket
            for key in token_bucket_params.keys()
            for bucket in bucket_config
        ):
            raise KeyError(
                f"Invalid configuration. Required keys for each bucket: {', '.join(token_bucket_params)}"
            )
        if not all(
            isinstance(bucket[param], token_bucket_params.get(param, ""))
            for param in token_bucket_params
            for bucket in bucket_config
        ):
            raise TypeError(
                f"Invalid configuration. Required types for each bucket: {', '.join([f'{x} - {formatannotation(y)}' for x, y in token_bucket_params.items()])}"
            )

    def _add_identifier(self, identifier: str) -> None:
        self._validate_identifier(identifier)
        if identifier not in self._buckets:
            self._buckets[identifier] = {}

    def add_bucket(self, identifier: str, bucket: TokenBucket) -> None:
        self._validate_add_bucket(bucket)
        self._add_identifier(identifier)
        bucket.identifier = identifier
        bucket.cost = self._cost
        self._buckets.add_bucket(bucket)

    def add_from_dict(
        self, identifier: str, bucket_config: list[dict[str, Any]]
    ) -> None:
        self._validate_add_from_dict(bucket_config)
        self._add_identifier(identifier)
        for bucket in bucket_config:
            token_bucket: TokenBucket = TokenBucket(
                replenish_time=int(bucket["replenish_time"]),
                max_tokens=int(bucket["max_tokens"]),
            )
            self.add_bucket(identifier, token_bucket)

    def consume(self, identifier: str) -> bool:
        self._validate_identifier(identifier)
        if identifier not in self._buckets.keys():
            raise KeyError(f"Invalid identifier: `{identifier}`")

        if not all(
            self._buckets.consume(identifier, bucket_key)
            for bucket_key in self._buckets[identifier].keys()
        ):
            return False

        return True

    def enable(self, identifier: str) -> Any:
        def wrapper(fn: Callable):
            if not asyncio.iscoroutinefunction(fn):

                def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return fn(*args, **kwargs)

                return inner
            else:

                async def inner(*args, **kwargs):
                    if not self.consume(identifier):
                        raise TokenThrottlerException()
                    return await fn(*args, **kwargs)

                return inner

        return wrapper
