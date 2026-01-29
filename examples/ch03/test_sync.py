import tempfile
from pathlib import Path
import shutil

from ch03.sync import sync, determine_actions
from ch03.filesystem import FakeFileSystem


class TestE2E:
    @staticmethod
    def test_when_a_file_exists_in_the_source_but_not_the_destination():
        try:
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a very useful file"
            (Path(source) / "my-file").write_text(content)

            sync(source, dest)

            expected_path = Path(dest) / "my-file"
            assert expected_path.exists()
            assert expected_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source():
        try:
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a file that was renamed"
            source_path = Path(source) / "source-filename"
            old_dest_path = Path(dest) / "dest-filename"
            expected_dest_path = Path(dest) / "source-filename"
            source_path.write_text(content)
            old_dest_path.write_text(content)

            sync(source, dest)

            assert old_dest_path.exists() is False
            assert expected_dest_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)


class TestWithFakeFileSystem:
    def test_when_a_file_exists_in_the_source_but_not_the_destination(self):
        source = Path("/source")
        dest = Path("/dest")
        fs = FakeFileSystem()
        fs.create_file(source / "my-file", "I am a very useful file")

        sync(source, dest, filesystem=fs)

        assert fs.exists(dest / "my-file")
        assert fs.read(dest / "my-file") == "I am a very useful file"

    def test_when_a_file_has_been_renamed_in_the_source(self):
        source = Path("/source")
        dest = Path("/dest")
        content = "I am a file that was renamed"
        fs = FakeFileSystem()
        fs.create_file(source / "source-filename", content)
        fs.create_file(dest / "dest-filename", content)

        sync(source, dest, filesystem=fs)

        assert not fs.exists(dest / "dest-filename")
        assert fs.exists(dest / "source-filename")
        assert fs.read(dest / "source-filename") == content

    def test_when_a_file_exists_in_dest_but_not_source(self):
        source = Path("/source")
        dest = Path("/dest")
        fs = FakeFileSystem()
        fs.create_file(dest / "obsolete-file", "I should be deleted")

        sync(source, dest, filesystem=fs)

        assert not fs.exists(dest / "obsolete-file")

    def test_records_actions(self):
        source = Path("/source")
        dest = Path("/dest")
        fs = FakeFileSystem()
        fs.create_file(source / "new-file", "new content")
        fs.create_file(dest / "old-file", "old content")

        sync(source, dest, filesystem=fs)

        assert ("COPY", source / "new-file", dest / "new-file") in fs.actions
        assert ("DELETE", dest / "old-file") in fs.actions


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]
