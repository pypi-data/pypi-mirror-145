from setuptools import setup

setup(
    name='postgresqlite',
    version='0.1.0',    
    description='Python package that gives you the power of a PostgreSQL server, with the convenience of the `sqlite3` package.',
    url='https://github.com/vanviegen/postgresqlite',
    author='Frank van Viegen',
    author_email='git@vanviegen.net',
    license='BSD 2-clause',
    packages=['postgresqlite'],
    install_requires=['pg8000 >= 1.24.1'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Database',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)