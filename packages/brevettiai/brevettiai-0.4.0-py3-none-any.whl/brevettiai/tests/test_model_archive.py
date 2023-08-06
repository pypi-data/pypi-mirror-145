import json
import os
import unittest

from brevettiai.tests.test_model_metadata import TestModelMetadata
from brevettiai.platform import ModelArchive
from tempfile import TemporaryDirectory


class TestModelArchive(unittest.TestCase):
    def test_write_archive(self):
        with TemporaryDirectory() as tmpdir:
            asset_name = "test"
            asset_content = b'test'
            testfile = os.path.join(tmpdir, "test.txt")
            with open(testfile, "wb") as fp:
                fp.write(asset_content)

            meta = json.loads(TestModelMetadata.image_segmentation_metadata[0])
            archive = ModelArchive(path=os.path.join(tmpdir, "test.tar.gz"), metadata=meta)

            self.assertRaises(FileNotFoundError, archive.open_read)

            with archive.open_write() as writer:
                self.assertRaises(IOError, archive.open_read)
                writer.add_asset(asset_name, "test.txt", testfile)

            with archive.open_read() as reader:
                self.assertRaises(IOError, archive.open_write)
                with reader.get_asset(asset_name) as fp:
                    assert fp.read() == asset_content


if __name__ == '__main__':
    unittest.main()
