from argparse import Action, ArgumentParser

known_drivers = ['local', 's3']

# within the parens after DriverAction, specify name of classes you inherit from
class DriverAction(Action):
    # here we are defining a method. a method is essentially a function inside of a class. variables in an object (in this case DriverAction) are called attributes in an object
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        # adding validation for anything other than local or s3
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Available drivers are 'local' & 's3'")
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help="URL of the PostgreSQL database to backup")
    parser.add_argument('--driver', '-d',
        help="how and where to store the backup",
        nargs=2,
        action=DriverAction,
        metavar=('driver', 'destination'),
        required=True)
    return parser

def main():
    import time
    import boto3
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}")
        storage.s3(client, dump.stdout, args.destination, file_name)
    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing database up locally to {args.destination}")
        storage.local(dump.stdout, outfile)