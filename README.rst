pgbackup
========

CLI for backing up remote PostgreSQL database either locally or to S3.

Preparing the Development
-------------------------

1. Ensure ``pip`` and ``pipenv`` are installed
2. Clone the repo: ``gitclone git@github.com:whompus/pgbackup``
3. ``cd`` into the repository
4. Fetch development dependencies ``make install``
5. Activate virtualenv: ``pipenv shell``

Usage
-----

Pass in a full databse URL, the storage driver, and the destination.

S3 Example w/ bucket name:

::

    $ pgbackup postgres://bob@example.com:5432/db_one --driver s3 backups

Local Example w/ local path:

::

    $ pgbackup postgres://bob@example.com:5432/db_one --driver local /var/local/db_one/backups/dump.sql


Running Tests
-------------

Run tests locally using ``make`` if virtualenv is active:

::

    $ make

If virtualenv isn't active then use:

::

    $ pipenv run make