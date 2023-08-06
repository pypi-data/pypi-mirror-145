import abc

from .. import TokenBucket


class BucketStorage(dict, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_bucket(self, bucket: TokenBucket) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def replenish(self, bucket: TokenBucket) -> None:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def consume(self, identifier: str, bucket_key: str) -> bool:  # pragma: no cover
        raise NotImplementedError()
