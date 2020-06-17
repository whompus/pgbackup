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
    parser.add_argument('--driver',
        help="how and where to store the backup",
        nargs=2,
        action=DriverAction,
        required=True)
    return parser