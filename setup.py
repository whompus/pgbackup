from setuptools import setup, find_packages

# this line is so that our README can be used as part of our package
with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='pgbackup',
    version='0.1.0',
    description='Databse backups locally or to AWS S3',
    long_description=readme,
    author='Mat',
    author_email='mat@example.com',
    install_requires=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pgbackup=pgbackup.cli:main',
        ],
    }
)