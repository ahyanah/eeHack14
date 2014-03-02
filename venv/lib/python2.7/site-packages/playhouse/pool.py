"""
Lightweight connection pooling for peewee.
"""
import heapq
import threading
import time


class ConnectionPool(object):
    def __init__(self,
                 database_constructor,
                 stale_timeout=None,
                 max_connections=64,
                 threadlocals=False):
        """
        :param database_constructor: A function which returns a newly-created
            :py:class:`Database` instance.
        :param int stale_timeout: Timeout after which a connection will be
            considered stale and reopened on the next access.
        :param int max_connections: Maximum number of connections to hold open.
        :param threadlocals: Repeated calls from a given thread will return the
            same connection.
        """
        self.constructor = database_constructor
        self.stale_timeout = stale_timeout
        self.max_connections = max_connections
        self.threadlocals = threadlocals
        self._connections = []
        self._in_use = {}

    def create_connection(self):
        if len(self._in_use) > self.max_connections:
            raise Exception('Too many connections.')
        return time.time(), self.constructor()

    def connect(self):
        try:
            ts, conn = heapq.heappop(self._connections)
        except IndexError:
            ts, conn = self.create_connection()
        if self.stale_timeout and (time.time() - ts) > stale_timeout:
            conn.close()
            ts, conn = self.create_connection()
        self._in_use[conn] = ts
        return conn

    def close(self, conn):
        ts = self._in_use[conn]
        del self._in_use[conn]
        heapq.heappush(self._connections, (ts, conn))

    def close_all(self):
        for _, conn in self._connections:
            conn.close()
        for conn in self._in_use:
            conn.close()
