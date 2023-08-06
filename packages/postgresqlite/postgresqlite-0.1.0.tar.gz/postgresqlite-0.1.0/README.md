# PostgreSQLite

Python module that gives you the power of a PostgreSQL server, with the convenience of the `sqlite3` module.

## Features

- Using just a `postgresqlite.connect()` call, the library will automatically...
    - Download and install PostgreSQL into the user's `~/.cache` directory.
    - Create a new database (`initdb`) within the project directory.
    - Start the PostgreSQL server and shut it down when it's no longer in use.
    - Set up a DB-API connection to the server (using the `pg8000` driver).
- It also adds a couple of conveniences on top of DB-API, inspired by the `sqlite3` module:
    - Calls to `fetchall` and `fetchone` return objects that can address fields both by number (as is standard for DB-API) as well as by name (as `sqlite3` offers when you configure `connection.row_factory = sqlite3.Row`).
- It can open `psql` and other PostgreSQL clients passing in connection details, while making sure the database is running.

## Examples

### Plain DB-API

### SQLAlchemy