from functools import wraps
import random
from contextlib import contextmanager
from time import sleep


def synthetic_latency(delay: float = 0.1):
    """A decorator that adds latency to a function.

    The function will be delayed `delay` seconds.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Simulating {delay} seconds latency...")
            sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def unstable(rate: float = 0.1):
    """A decorator that makes a function unstable.

    The function will fail with a probability of `rate`.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if random.random() < rate:
                print("Simulating an unstable function...")
                raise Exception("Unstable function failed")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@contextmanager
def retry(max_attempts: int, delay: float):
    """
    A context manager that retries a block of code.
    """
    attempt = 0
    while attempt < max_attempts:
        try:
            print(f"Attempt {attempt + 1}/{max_attempts}...")
            yield
            break
        except Exception:
            attempt += 1
            print(f"caught an exception ({attempt}), retrying...")
            sleep(delay)
    else:
        # Raise an exception if the maximum number of attempts is reached
        raise Exception(f"Failed after {max_attempts} attempts.")
