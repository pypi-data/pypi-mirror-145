from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Any, cast

import portalocker
from colorama.ansi import Fore

from beni import WrappedFunc, crc_str, getpath_workspace, hold, makedir, remove
from beni.print import print_color


@contextmanager
def lockkey(*keys: str, timeout: float = 0, quite: bool = False):
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


def w_lockkey(*keys: str, timeout: float = 0, quite: bool = False):
    def wraperfun(func: WrappedFunc) -> WrappedFunc:
        @wraps(func)
        def wraper(*args: Any, **kwargs: Any):
            with lockkey(*keys, timeout=timeout, quite=quite):
                return func(*args, **kwargs)
        return cast(WrappedFunc, wraper)
    return wraperfun


def lock_acquire(key: str, timeout: float = 0, quite: bool = False):
    '''不对外部提供，只提供给 async_keylock 方法使用'''
    keyfile = getpath_workspace(f'.lock/{crc_str(key)}.lock')
    makedir(keyfile.parent)
    while True:
        try:
            lock = portalocker.Lock(keyfile, timeout=timeout, fail_when_locked=timeout == 0)
            f = lock.acquire()
            f.write(key)
            f.flush()
            break
        except:
            if quite:
                raise Exception(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}')
            else:
                print_color(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}', colorList=[Fore.LIGHTRED_EX])
                inputvalue = hold(f'重试（retry）或退出（exit）', False, 'retry', 'exit')
                match inputvalue:
                    case 'retry':
                        print('正在重试...')
                    case 'exit':
                        raise Exception(f'资源被锁定无法继续操作 - {key}')
                    case _:
                        pass
    return lock, keyfile
