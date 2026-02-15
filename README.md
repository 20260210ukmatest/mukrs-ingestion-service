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

This ingests tournaments in a particular range of ids (as defined by EMA). This is useful for initial seeding of the database. For example, to ingest all tournaments from 2023 to 2025:

```shell
python ingest_by_id.py 285 404
```

## Notes on implementation

### Ingestion routine

- When ingesting data for a tournament which has already been ingested, the routine attempts to compare the existing and ingested data. If identical, ingestion is skipped. If different, data is re-ingested as a new _version_ of the tournament. The old version is maintained for later inspection / diff views.
- For simplicity and future flexibility, all players' data is ingested, even non-UK players.

### Database structure

- `tournaments` - holds tournament metadata. In particular, one row of `tournaments` is a _version_ of the metadata for one tournament from one ingestion run.
  - `id` - primary key column for the table.
  - `ema_id` - this is the EMA's own identifier for each tournament.
  - `ingested_on` - the date and time of ingestion for this data.
  - `is_latest` - a bool flag indicating whether or not this is the latest data for this tournament (identified by the `ema_id`). This makes querying all tournaments more efficient. Each `ema_id` should only have one row where this is set to true - it is set to false when a new version of data for the same `ema_id` is ingested.
  - `excluded_from_ingestion` - when this is set to true on the latest row for a tournament, the tournament is skipped by subsequent ingestion runs. This allows us to take manual control of certain tournaments' data where we know there is an issue and we do not expect that it will be rectified
- `players` - holds player metadata.
- `tournament_results` - holds the base ranks achieved by players at tournaments.
