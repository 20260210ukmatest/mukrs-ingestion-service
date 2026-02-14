# MUKRS Ingestion Service

Read MERS tournament data from the EMA website and save it in a database.

## Setup

### Dependencies

Ensure you have Python installed (>=3.7). Then install required packages:

```shell
pip install -r requirements.txt
```

### Database

Create a PostgreSQL database and run the commands found in `init.sql`.

Provide the connection string in a `DBCONN` environment variable or modify the default connection string in `services/get_dbconn.py`.

## Usage

### `ingest_most_recent.py`

This ingests tournament data from the last 6 months.

```shell
python ingest_most_recent.py
```

### `ingest_by_id.py`

This ingests tournaments in a particular range of ids (as defined by EMA). This is useful for initial seeding of the database.

```shell
python ingest_by_id.py 218 363
```
