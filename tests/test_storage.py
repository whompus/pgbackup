import tempfile
import pytest

from pgbackup import storage

@pytest.fixture
def infile():
    f = tempfile.TemporaryFile()
    f.write(b'Testing')
    f.seek(0)
    return f

def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """

    # delete=False because if we leave it as the default of true, 
    # then it's going to be deleted as soon as we close the file.
    # We want our local method to close both of the files that 
    # it's given once it's completed.
    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)

    with open(outfile.name, 'rb') as f:
        assert f.read() == b'Testing'

def test_storing_file_on_s3(mocker, infile):
    """
    Write content from one file-like to S3
    """
    client = mocker.Mock()

    storage.s3(client, infile, "bucket", "file-name")

    client.upload_fileobj.assert_called_with(infile, "bucket", "file-name")
