# How to query data from MongoDB in real time

Tested with `Python 3.6.9` on [MongoDB Atlas Database-as-a-Service.](https://docs.atlas.mongodb.com/)

To run the `ETL`:

```
export MONGODB_USERNAME=sandbox
export MONGODB_PASSWORD=<replace with your password>
export API_CODE=<>
python src/python/census_etl_mongo.py --year <year> --mongo <y or n>
```

To run the `Change Stream`:

```
export MONGODB_USERNAME=sandbox
export MONGODB_PASSWORD=<replace with your password>
python src/python/census_change_stream.py
```

To configure and run the `MongoDB Materialized View`:
- Open a connection to the MongoDB Atlas with mongo shell.
- Copy & paste the contents of `mongodb-realtime-tutorial/src/mongoshell/census_mat_view.sh` one at a time.