"""
Dummy MongoDB backend for Django.

Usage
-----
Now django.db.connections['DB'].cursor() becomes available as a mongodb client connection (pymongo).

Limitation
----------
This Engine works up to the point of creating the db connections, taking in DATABASES options from your settings.py
The ORM layer (migration, schema, transactions, save/delete()) will not work on databases that has settings using this Engine.

Note that this is uncharted territory, Django has a hidden db backend mini framework. (Just like auth and storage)

@author Tim Lauv
@created 2017.03.13
"""

from pymongo import MongoClient
from django.db.backends.dummy.base import DatabaseWrapper as DummyBaseDatabaseWrapper

class DatabaseWrapper(DummyBaseDatabaseWrapper):
	"""docstring for DatabaseWrapper"""
	
	vendor = 'mongodb'
	
	# recover useful BaseDatabaseWrapper methods
	
	ensure_connection = DummyBaseDatabaseWrapper.ensure_connection
	_cursor = DummyBaseDatabaseWrapper._cursor
	_close = DummyBaseDatabaseWrapper._close

	# override/implement required methods

	def get_connection_params(self):
		"""TODO: DATABASES options: 
			NAME(db), HOST(host)/SOCK(sock), PORT(port), USER(user), PASSWORD(password), ...

			ref: http://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
		"""
		pass

	def get_new_connection(self, conn_params):
		"""TODO: use pymongo MongoClient to create a connection to a named db"""
		pass

	def init_connection_state(self):
		"""no state to be init-ed"""
		pass

	def create_cursor(self, name):
		"""create a cursor on collection [name]"""
		return self.connection[name]

	def _prepare_cursor(self, cursor):
		"""validate and simply return the cursor obtained by create_cursor()"""
		self.validate_thread_sharing()
		return cursor

	def _set_autocommit(self, autocommit):
		"""keep self.autocommit=False"""
		pass
