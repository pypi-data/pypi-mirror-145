from traceback import print_exc
from typing import Any, Callable, Optional, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


def tryfunc(
    f: Callable[..., T], default: Optional[U] = None
) -> Callable[..., Union[T, U, None]]:
    def wrapper(*args: Any, **kwargs: Any) -> Union[T, U, None]:
        try:
            return f(*args, **kwargs)
        # pylint: disable=W0702
        # We explicitly catch all exceptions here,
        # since we don't know what can happen inside `f`.
        # Note that Exception does not includes KeyboardInterrupt,
        # which inherits from BaseException.
        except Exception:
            print_exc()
            return default

    return wrapper


def unwrap(x: Optional[T]) -> T:
    if not x:
        raise ValueError(f"Unwrapped None value")
    return x
