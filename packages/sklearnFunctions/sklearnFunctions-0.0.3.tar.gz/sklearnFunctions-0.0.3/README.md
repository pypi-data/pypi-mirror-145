# mongoops - eleka12

This package built on top of pymongo to make ease of using MongoDB atlas operations.

# How to use mongoops

* install the latest package 

> * in jupyter notebook -
```
    !pip install mongoops
```

> * in command prompt -
```bash    
    pip install mongoops
```

* Now run below snippets of code in your jupyter-notebooks / python project to use pytorch defined functions

## Importing mongoops

```python

from mongoops.ops import MongoDBOperation

```

## Use your MongoDB atlas Database username / Password and atlas URL

```python

USERNAME = " "

PASSWORD = " "

URL = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.ornbe.mongodb.net/test"

```

## Creating a mongo client

```python

mongo=MongoDBOperation(atlas_url=URL)

client=mongo.get_database_client_object()

```

## Creating a database using mongoDB client

```python

DB=mongo.create_database(client,"DB_name")

COLLECTION=mongo.create_collection_in_database(DB,"collection_name")

mongo.create_record(COLLECTION,{"val":"mongoops"})

```

## Checking for DB presence 

```python

mongo.is_database_present(client,"DB_name")

```

## Checking for collection inside DataBase

```python

mongo.is_collection_present("collection_name",DB)

```

## pypi repo link -

[mongoops - PYPI](https://pypi.org/project/mongoops/)

## Github repo link - 

[mongoops - Github](https://github.com/Karthik-VG/mongo_lib/)


