from pathlib import Path
from typing import Final

import aiofiles

from beni import crc_bytes, getpath, makedir, md5_bytes
from beni.async_func import set_a_limit, wa_limit

LIMIT_TAG_FILE: Final = 'file'

set_a_limit(LIMIT_TAG_FILE, 50)


@wa_limit(LIMIT_TAG_FILE)
async def a_writefile_text(file: Path | str, content: str, encoding: str = 'utf8', newline: str = '\n'):
    if type(file) is not Path:
        file = getpath(file)
    makedir(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


@wa_limit(LIMIT_TAG_FILE)
async def a_writefile_bytes(file: Path | str, data: bytes):
    if type(file) is not Path:
        file = getpath(file)
    makedir(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


@wa_limit(LIMIT_TAG_FILE)
async def a_readfile_text(file: Path | str, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


@wa_limit(LIMIT_TAG_FILE)
async def a_readfile_bytes(file: Path | str):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


async def a_md5file(file: Path | str):
    return md5_bytes(
        await a_readfile_bytes(file)
    )


async def async_crcfile(file: Path | str):
    return crc_bytes(
        await a_readfile_bytes(file)
    )
