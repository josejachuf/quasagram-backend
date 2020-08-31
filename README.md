# quasagram-backend

This development is to be used (with some modifications) by the front end of the course on PWA of https://dannys.link/quasarpwa

The emmett framework is used with the emmett-rest extension (https://emmett.sh/)

Requires python3.8

## About the Database


There are many options about the database engine that you can use. For convenience we will use sqlite3 in this example. You can see more of this at: https://emmett.sh/docs/2.0.x/orm

The database is already created and its tables can use what is shown in the course

Users are not being managed, but the user_id field was introduced in the subscritions table

The jwt tokens are not used either, but if you need help to implement it please let us know

## Generate VAPID-Key

Create the private and public keys with:

```
$ openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem

$ openssl ec -in vapid_private.pem -pubout -out vapid_public.pem

$ openssl ec -in ./vapid_private.pem -outform DER|tail -c +8|head -c 32|base64|tr -d '=' |tr '/+' '_-' >> private_key.txt

$ openssl ec -in ./vapid_private.pem -pubout -outform DER|tail -c 65|base64|tr -d '=' |tr '/+' '_-' >> public_key.txt
```

Use the keys generated in the /models/posts.py file

## Notes

In a production environment notifications should be made using a task queue such as celery, for simplicity it is used directly when creating the post

## Install and run
```
$ python3.8 -m venv venv

$ source venv/bin/activate

$ emmett -a backend develop
```