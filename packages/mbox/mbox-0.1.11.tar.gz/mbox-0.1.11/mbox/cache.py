import pickle
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, TypeVar

from appdirs import user_cache_dir

U = TypeVar("U")


class Cache:
    """
    Simple cache that associates to a key the return value of a function.
    On Linux, files are stored in ~/.cache/{name}.
    """

    def __init__(self, name: str):
        self.dir = Path(user_cache_dir(name))
        self.dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def filename(key: str) -> str:
        key_ = key.encode("utf-8")
        return sha256(key_).digest().hex() + ".pkl"

    def filepath(self, key: str) -> Path:
        name = self.filename(key)
        return self.dir.joinpath(name)

    def flush(self) -> None:
        for file in self.dir.glob("*.pkl"):
            file.unlink()

    def get(
        self,
        key: str,
        fn: Callable[..., U],
        maxage: timedelta = timedelta(days=1),
        invalidate: bool = False,
    ) -> U:
        file = self.filepath(key)
        # 1) If the file exists, and it is expired, then delete it.
        if file.exists():
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            expired = datetime.now() - mtime > maxage
            if invalidate or expired:
                file.unlink()

        # 2) If the file does not exists, run the function and create it.
        if not file.exists():
            value_ = fn()
            with file.open("wb") as f:
                pickle.dump(value_, f)

        # 3) Return the value from the file.
        with file.open("rb") as f:
            value: U = pickle.load(f)

        return value


class NoopCache(Cache):
    """
    A cache that... doesn't cache.
    """

    def get(self, key: str, fn: Callable[..., U], *args: Any, **kwargs: Any) -> U:
        return fn()
