from datetime import datetime, timezone

from .. import TokenBucket
from . import BucketStorage


class RuntimeStorage(BucketStorage):
    def add_bucket(self, bucket: TokenBucket) -> None:
        self[bucket.identifier][str(bucket.replenish_time)] = bucket

    def replenish(self, bucket: TokenBucket):
        current_time: float = datetime.now(timezone.utc).timestamp()

        if (current_time < bucket.last_replenished) or (
            current_time - bucket.last_replenished < bucket.replenish_time
        ):
            return

        bucket.last_replenished = current_time
        bucket.tokens = bucket.max_tokens

    def consume(self, identifier: str, bucket_key: str) -> bool:
        bucket: TokenBucket = self[identifier][str(bucket_key)]
        self.replenish(bucket)
        return bucket.consume()
