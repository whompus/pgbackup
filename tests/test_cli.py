import pytest
from pgbackup import cli

# below is what we eventually want to be able to do
# $ pgbackup postgres://bob@example.com:5432/db_one --driver s3 backups

url = "postgres://bob@example.com:5432/db_one"

# create fixture with decorator, more info on decorators here: https://www.reddit.com/r/Python/comments/2lrhp5/could_someone_give_me_an_eli5_for_decorators/clxgkce/
@pytest.fixture
def parser():
    return cli.create_parser()

def test_parser_without_driver(parser):
    """
    Asserting a certain error will happen.
    Without a specified driver, the parser will exit
    SystemExit happens when a parser fails.
    What needs to happen for us to exercise this?
        - Need to create a parser
        - Then parse_args, because that's what checks to see if the URL exists
    """
    with pytest.raises(SystemExit):
        # create parser before the arguments have been parsed
        parser.parse_args([url])

def test_parser_with_driver(parser):
    """
    The parser will exit if it recieves a driver without a destination
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])

def test_parser_with_unknow_driver(parser):
    """
    The parser will exit if the driver name is unknown
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, '--driver', 'azure', 'destination'])

# another happy path test:
def test_parser_with_known_drivers(parser):
    """
    The parser will not exit if the driver name is known
    """
    for driver in ['local', 's3']:
        parser.parse_args([url, '--driver', driver, 'destination'])

# happy path test:
def test_parser_with_driver_and_destination(parser):
    """
    The parser will not exit if it recieves a driver and destination
    """
    args = parser.parse_args([url, '--driver', 'local', '/some/path'])
    
    assert args.url == url
    assert args.driver == 'local'
    assert args.destination == '/some/path'