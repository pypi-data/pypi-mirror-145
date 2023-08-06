import random
from itertools import repeat, takewhile
from typing import IO, Callable, Generator, List


def idx(b: bytes, offset: int = 0) -> List[int]:
    err = False
    start = 0
    indices = []
    while not err:
        try:
            index = b.index(b"\n", start)
            indices.append(offset + index)
            start = index + 1
        except:
            err = True
    return indices


def indices_of_newlines(fp: IO) -> List[int]:
    size = 1024 * 1024
    bufgen = takewhile(lambda x: x, (fp.read(size) for _ in repeat(None)))
    indices = []
    for i, buf in enumerate(bufgen):
        indices.extend(idx(buf, i * size))
    return indices


def readline(
    filepath: str,
    shuffle: bool = True,
    chunk_size: int = 1,
    opener: Callable[[str, str], IO] = open,
):
    chunk_size = chunk_size or 1
    with opener(filepath, "rb") as b:
        indices = [-1, *indices_of_newlines(b)]
        blocks = list(range(0, len(indices), chunk_size))

    def gen() -> Generator[str, None, None]:
        _blocks = [*blocks]
        _size = len(_blocks)
        with opener(filepath, "rt") as t:
            while _size:
                block_index = (
                    random.randrange(_size) if shuffle else len(_blocks) - _size
                )
                index = _blocks[block_index]
                _blocks[block_index] = _blocks[_size - 1]
                _size -= 1
                t.seek(indices[index] + 1)
                for _ in range(chunk_size):
                    line = t.readline()
                    if line:
                        yield line

    return len(indices) - 1, gen
