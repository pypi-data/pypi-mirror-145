from abc import ABC, abstractmethod

import requests

from biolib.typing_utils import Iterable


class IndexableBuffer(ABC):

    def __init__(self):
        self.pointer = 0

    @abstractmethod
    def get_data(self, start: int, end: int) -> bytes:
        pass

    @abstractmethod
    def get_data_as_iterable(self, start: int, end: int, chunk_size: int) -> Iterable[bytes]:
        pass

    def get_data_as_string(self, start: int, end: int) -> str:
        return self.get_data(start=start, end=end).decode()

    def get_data_as_int(self, start: int, end: int) -> int:
        return int.from_bytes(bytes=self.get_data(start=start, end=end), byteorder='big')

    def get_data_with_pointer(self, length_bytes: int) -> bytes:
        data = self.get_data(start=self.pointer, end=self.pointer + length_bytes)
        self.pointer += length_bytes
        return data

    def get_data_with_pointer_as_int(self, length_bytes: int) -> int:
        data = self.get_data_as_int(start=self.pointer, end=self.pointer + length_bytes)
        self.pointer += length_bytes
        return data

    def get_data_with_pointer_as_string(self, length_bytes: int) -> str:
        data = self.get_data_as_string(start=self.pointer, end=self.pointer + length_bytes)
        self.pointer += length_bytes
        return data


class RemoteIndexableBuffer(IndexableBuffer):

    def __init__(self, url: str):
        super().__init__()
        self._url = url

    def get_data(self, start: int, end: int) -> bytes:
        expected_length = end - start + 1
        if expected_length < 0:
            raise Exception(f'get_data got invalid range: {start}-{end}')

        if expected_length == 0:
            return bytes(0)

        response = requests.get(url=self._url, headers={'range': f'bytes={start}-{end}'})
        if not response.ok:
            raise Exception(f'get_data got not ok response status {response.status_code}')

        data: bytes = response.content
        if len(data) != expected_length:
            raise Exception(f'get_data got response of unexpected length. Got {len(data)} expected {expected_length}.')

        return data

    def get_data_as_iterable(self, start: int, end: int, chunk_size: int) -> Iterable[bytes]:
        expected_length = end - start
        if expected_length < 0:
            raise Exception(f'get_data got invalid range: {start}-{end}')

        if expected_length == 0:
            return []

        response = requests.get(
            url=self._url,
            headers={'range': f'bytes={start}-{end}'},
            stream=True,
            timeout=60,
        )
        return response.iter_content(chunk_size=chunk_size)


class InMemoryIndexableBuffer(IndexableBuffer):

    def __init__(self, data: bytes):
        super().__init__()
        self._buffer = data
        self._length_bytes = len(data)

    def get_data(self, start: int, end: int) -> bytes:
        return self._buffer[start:end]

    def get_data_as_iterable(self, start: int, end: int, chunk_size: int) -> Iterable[bytes]:
        raise NotImplementedError

    def __len__(self):
        return self._length_bytes


class LazyLoadedFile:

    def __init__(self, path: str, buffer: IndexableBuffer, start: int, end: int):
        self._path = path
        self._buffer = buffer
        self._start = start
        self._end = end

    @property
    def path(self) -> str:
        return self._path

    def get_data(self) -> bytes:
        return self._buffer.get_data(start=self._start, end=self._end)

    def get_data_as_iterable(self) -> Iterable[bytes]:
        return self._buffer.get_data_as_iterable(start=self._start, end=self._end, chunk_size=1_000_000)
