import abc
import hashlib
import os
import shutil
from pathlib import Path


BLOCKSIZE = 65536


class AbstractFileSystem(abc.ABC):
    @abc.abstractmethod
    def read_paths_and_hashes(self, root: Path) -> dict[str, str]:
        """Return a dict mapping hash -> filename for all files under root."""
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self, src: Path, dest: Path) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def move(self, src: Path, dest: Path) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, path: Path) -> None:
        raise NotImplementedError


class RealFileSystem(AbstractFileSystem):
    @staticmethod
    def _hash_file(path: Path) -> str:
        hasher = hashlib.sha1()
        with path.open("rb") as file:
            buf = file.read(BLOCKSIZE)
            while buf:
                hasher.update(buf)
                buf = file.read(BLOCKSIZE)
        return hasher.hexdigest()

    def read_paths_and_hashes(self, root: Path) -> dict[str, str]:
        hashes = {}
        for folder, _, files in os.walk(root):
            for fn in files:
                hashes[self._hash_file(Path(folder) / fn)] = fn
        return hashes

    def copy(self, src: Path, dest: Path) -> None:
        shutil.copyfile(src, dest)

    def move(self, src: Path, dest: Path) -> None:
        shutil.move(src, dest)

    def delete(self, path: Path) -> None:
        os.remove(path)


class FakeFileSystem(AbstractFileSystem):
    def __init__(self):
        self.files: dict[Path, str] = {}  # path -> content
        self.actions: list[tuple] = []    # recorded actions for assertions

    def create_file(self, path: Path, content: str) -> None:
        """Helper to set up test fixtures."""
        self.files[path] = content

    def _hash_content(self, content: str) -> str:
        return hashlib.sha1(content.encode()).hexdigest()

    def read_paths_and_hashes(self, root: Path) -> dict[str, str]:
        hashes = {}
        for path, content in self.files.items():
            if str(path).startswith(str(root)):
                hashes[self._hash_content(content)] = path.name
        return hashes

    def copy(self, src: Path, dest: Path) -> None:
        self.actions.append(("COPY", src, dest))
        self.files[dest] = self.files[src]

    def move(self, src: Path, dest: Path) -> None:
        self.actions.append(("MOVE", src, dest))
        self.files[dest] = self.files[src]
        del self.files[src]

    def delete(self, path: Path) -> None:
        self.actions.append(("DELETE", path))
        if path in self.files:
            del self.files[path]

    def exists(self, path: Path) -> bool:
        return path in self.files

    def read(self, path: Path) -> str:
        return self.files[path]
