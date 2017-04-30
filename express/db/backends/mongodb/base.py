"""
Dummy MongoDB backend for Django.

Usage
-----
Put this engine in your DATABASES in the settings.py

DATABASES = {
    ...,
    'mongo': {
        'ENGINE': 'express.db.backends.mongodb',
        'HOST': 'mongo.server.com',
        'PORT': 27017,
        'NAME': 'testdb',
        'USER': '...',
        'PASSWORD': '...',
        'OPTIONS': {
            ...pymongo.MongoClient options...
        }
    },
    ...
}

Now you will have,
* django.db.connections['testdb'].db becomes available as a pymongo db;
* django.db.connections['testdb'].collection('collection'=None) becomes available as a pymongo collection;
* django.db.connections['testdb'].cursor('collection', **kwargs) becomes available as a .find(kwargs) pymongo cursor;
After getting the above, you will have,
* django.db.connections['testdb'].connection becomes available as pymongo client;


Limitation
----------
This Engine works up to the point of creating the db connection and collection cursor, taking in DATABASES options from your settings.py;
The ORM layer (migration, schema, transactions, save/delete()) will not work on database that has settings using this Engine.

Note that this is uncharted territory, Django has a hidden db backend mini framework. (Just like auth and storage)

@author Tim Lauv
@created 2017.03.13
"""

from urllib.parse import quote_plus
from pymongo import MongoClient
from django.db.backends.dummy.base import DatabaseWrapper as DummyBaseDatabaseWrapper


class DatabaseWrapper(DummyBaseDatabaseWrapper):
    """docstring for DatabaseWrapper"""

    vendor = 'mongodb'
    Database = MongoClient

    # recover useful BaseDatabaseWrapper methods

    def ensure_connection(self):
        return super(DummyBaseDatabaseWrapper, self).ensure_connection()

    # override/implement required methods

    def get_connection_params(self):
        """
        DATABASES options:
            NAME(db), HOST(host), PORT(port), USER(user), PASSWORD(password), DOC_CLASS(document_class), TZ_AWARE(tz_aware), CONNECT(connect)
            OPTIONS(other kwargs to MongoClient)

            ref: http://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
        """
        kwargs = {
            'host': 'localhost',
            'port': 27017,
            'tz_aware': False,
            'connect': True,
            'document_class': dict,
        }
        settings_dict = self.settings_dict

        if settings_dict['NAME']:
            self._dbname = settings_dict['NAME']
        if settings_dict['HOST']:
            kwargs['host'] = settings_dict['HOST']
        if settings_dict['PORT']:
            kwargs['port'] = settings_dict['PORT']
        if settings_dict['USER']:
            kwargs['host'] = 'mongodb://{}:{}@{}'.format(
                quote_plus(settings_dict['USER']), quote_plus(settings_dict['PASSWORD']), kwargs['host']
            )
        if 'DOC_CLASS' in settings_dict:
            kwargs['document_class'] = settings_dict['DOC_CLASS']
        if 'TZ_AWARE' in settings_dict:
            kwargs['tz_aware'] = settings_dict['TZ_AWARE']
        if 'CONNECT' in settings_dict:
            kwargs['connect'] = settings_dict['CONNECT']

        options = settings_dict['OPTIONS'].copy()
        kwargs.update(options)
        return kwargs

    def get_new_connection(self, conn_params):
        """use pymongo MongoClient to create a connection (a client object)"""
        return MongoClient(**conn_params)

    def init_connection_state(self):
        """no state to be init-ed"""
        pass

    def create_cursor(self, name, **kwargs):
        """create a cursor on collection [name] by find(**kwargs)"""
        return self.db[name].find(kwargs)

    # override wrappers for PEP-249 connection methods

    def _prepare_cursor(self, cursor):
        """validate and simply return the cursor obtained by create_cursor()"""
        self.validate_thread_sharing()
        return cursor

    def _cursor(self, name, **kwargs):
        """pick a collection by name and return the find() cursor"""
        self.ensure_connection()
        with self.wrap_database_errors:
            return self.create_cursor(name, **kwargs)

    def _close(self):
        """close the db.client"""
        if self.connection is not None:
            with self.wrap_database_errors:
                return self.connection.close()

    def cursor(self, name, **kwargs):
        """create a cursor"""
        return self._cursor(name, **kwargs)

    # extras by Tim (+.collection(), +.db)

    def collection(self, name=None):
        """return a collection handle by name"""
        self.ensure_connection()
        with self.wrap_database_errors:
            if name:
                return self.db[name]
            else:
                return self.db.collection_names(False)  # show only user created collections (no system.*)

    @property
    def db(self):
        """return the db handle"""
        self.ensure_connection()
        with self.wrap_database_errors:
            return self.connection[self._dbname]

    # override transaction methods

    def _set_autocommit(self, autocommit):
        """keep self.autocommit=False"""
        pass
