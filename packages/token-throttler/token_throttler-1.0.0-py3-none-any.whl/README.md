# Token throttler

![Coverage](https://img.shields.io/gitlab/coverage/vojko.pribudic/token-throttler/main?job_name=tests)
![Version](https://img.shields.io/pypi/pyversions/token-throttler)
![Downloads](https://pepy.tech/badge/token-throttler)
![License](https://img.shields.io/pypi/l/token-throttler)

**Token throttler** is an extendable rate-limiting library somewhat based on a [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket).

## Table of contents

1. [ Installation ](#installation)
2. [ Features ](#features)
3. [ Usage ](#usage)
    1. [ Manual usage example ](#usage-manual)
    2. [ Decorator usage example ](#usage-decorator)
4. [ Storage ](#storage)
   1. [ Redis storage example ](#storage-redis)

<a name="installation"></a>
## 1. Installation

Token throttler is available on PyPI:
```console 
$ python -m pip install token-throttler
```
Token throttler officially supports Python >= 3.7.

<a name="features"></a>
## 2. Features

- Configurable token throttler cost and identifier
- Multiple buckets per throttler per identifier
- Buckets can be added manually or by a `dict` configuration
- Manual usage or usage via decorator
- Decorator usage supports async code too
- Custom decorator can be written
- Extendable storage engine (eg. Redis)

<a name="usage"></a>
## 3. Usage

Token throttler supports both manual usage and via decorator.

Decorator usage supports both async and sync.

<a name="usage-manual"></a>
### 1) Manual usage example:

```python
from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(cost=1, storage=RuntimeStorage())
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=10, max_tokens=10))
throttler.add_bucket(identifier="hello_world", bucket=TokenBucket(replenish_time=30, max_tokens=20))


def hello_world() -> None:
    print("Hello World")


for i in range(10):
    throttler.consume(identifier="hello_world")
    hello_world()

if throttler.consume(identifier="hello_world"):
    hello_world()
else:
    print("bucket_one ran out of tokens")
```

<a name="usage-decorator"></a>
### 2) Decorator usage example:

```python
from token_throttler import TokenBucket, TokenThrottler, TokenThrottlerException
from token_throttler.storage import RuntimeStorage

throttler: TokenThrottler = TokenThrottler(1, RuntimeStorage())
throttler.add_bucket("hello_world", TokenBucket(10, 10))
throttler.add_bucket("hello_world", TokenBucket(30, 20))


@throttler.enable("hello_world")
def hello_world() -> None:
    print("Hello World")


for i in range(10):
    hello_world()

try:
    hello_world()
except TokenThrottlerException:
    print("bucket_one ran out of tokens")
```

For other examples see [**examples**](https://gitlab.com/vojko.pribudic/token-throttler/-/tree/main/examples) directory.

<a name="storage"></a>
## 4. Storage

Currently, token throttler supports `RuntimeStorage` but is very easy to extend.
If you want your own storage engine, feel free to extend the `token_throttler.storage.BucketStorage` class.

<a name="storage-redis"></a>
### 1) Redis storage example:

```python
import pickle
from datetime import timedelta
from typing import Union

from redis import StrictRedis

from token_throttler import TokenBucket, TokenThrottler
from token_throttler.storage import BucketStorage


class RedisStorage(BucketStorage):
    def __init__(self, connection_string: str, delimiter: str) -> None:
        super().__init__()
        self.redis: StrictRedis = StrictRedis.from_url(url=connection_string)
        self.delimiter: str = delimiter

    def _save_bucket(self, cache_key: str, bucket: TokenBucket) -> None:
        self.redis.setex(
            cache_key,
            timedelta(seconds=bucket.replenish_time),
            pickle.dumps(bucket),
        )

    def _get_bucket(self, cache_key: str):
        bucket: Union[bytes, None] = self.redis.get(cache_key)
        if not bucket:
            bucket_info: list[str] = cache_key.split(self.delimiter)
            token_bucket: TokenBucket = TokenBucket(
                int(bucket_info[1]), int(bucket_info[-1])
            )
            token_bucket.cost = int(bucket_info[2])
            token_bucket.identifier = bucket_info[0]
            return token_bucket
        return pickle.loads(bucket)

    def add_bucket(self, bucket: TokenBucket) -> None:
        cache_key: str = f"{self.delimiter}".join(
            map(
                str,
                [
                    bucket.identifier,
                    bucket.replenish_time,
                    bucket.cost,
                    bucket.max_tokens,
                ],
            )
        )
        self[bucket.identifier][str(bucket.replenish_time)] = cache_key
        self._save_bucket(cache_key, self._get_bucket(cache_key))

    def replenish(self, bucket: TokenBucket) -> None:
        pass

    def consume(self, identifier: str, bucket_key: str) -> bool:
        cache_key: str = self[identifier][str(bucket_key)]
        bucket: TokenBucket = self._get_bucket(cache_key)
        bucket_state: bool = bucket.consume()
        self._save_bucket(cache_key, bucket)
        return bucket_state


throttler: TokenThrottler = TokenThrottler(1, RedisStorage(connection_string="connection-string-to-redis", delimiter="||"))
...
```