from distutils.core import setup

setup(
    name='RunPsqlScripts',
    version='0.3.2',
    description='Library for python 3 that allows to execute queries for PostgreSQL according to the load definition',
    author='Juan Rueda',
    author_email='Juan.Rueda@btgpactual.com',
    packages=['RunPsqlScripts'],
    license='MIT',
    install_requires=[
        'psycopg2-binary',
        'python-dotenv',
        'pyaml',
        'jsonschema',
        'colorlog'
    ],
    keywords=['postgresql']
)
