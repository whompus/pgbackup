import pytest
import subprocess
from pgbackup import pgdump

url = "postgres://bob:password@example.com:5432/db_one"

# test with mocking, calling the mocker fixture in our function
def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with the databse URL
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout=subprocess.PIPE)

def test_dump_handles_oserror(mocker):
    """
    pgdump.dump returns a resonable error if pg_dump isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

def test_dump_file_name_without_timestamp():
    """
    pgdump.dump_file_name returns the name of the database
    """
    assert pgdump.dump_file_name(url) == "db_one.sql"

def test_dump_file_name_with_timestamp():
    """
    pgdump.dump_file_name returns the name of the database with timestamp
    """
    timestamp = "2020-06-23T14:30:10"
    assert pgdump.dump_file_name(url, timestamp) == f"db_one-{timestamp}.sql"