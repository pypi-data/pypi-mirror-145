import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, cast

import portalocker

from beni import WrappedAsyncFunc, remove
from beni.lock import lock_acquire


@asynccontextmanager
async def a_lockkey(*keys: str, timeout: float = 0, quite: bool = False):
    lock_list: list[portalocker.Lock] = []
    keyfile_list: list[Path] = []
    for key in keys:
        lock, keyfile = lock_acquire(key, timeout, quite)
        lock_list.append(lock)
        keyfile_list.append(keyfile)
    try:
        yield
    finally:
        for lock in lock_list:
            lock.release()
        for keyfile in keyfile_list:
            try:
                remove(keyfile)
            except:
                pass


def wa_lockkey(*keys: str, timeout: float = 0, quite: bool = False):
    def wraperfun(func: WrappedAsyncFunc) -> WrappedAsyncFunc:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            async with a_lockkey(*keys, timeout=timeout, quite=quite):
                return await func(*args, **kwargs)
        return cast(WrappedAsyncFunc, wraper)
    return wraperfun


_locknum_dict: dict[int, int] = {}


def wa_locknum(num: int = 3):
    def wraperfun(func: WrappedAsyncFunc) -> WrappedAsyncFunc:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            func_id = id(func)
            while True:
                count = _locknum_dict.get(func_id, 0)
                if count < num:
                    _locknum_dict[func_id] = count + 1
                    result = await func(*args, **kwargs)
                    _locknum_dict[func_id] -= 1
                    return result
                else:
                    await asyncio.sleep(0)
        return cast(WrappedAsyncFunc, wraper)
    return wraperfun
