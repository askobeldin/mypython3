# ZODB - a native object database for Python #

Because ZODB is an object database:

*   no separate language for database operations

*   very little impact on your code to make objects persistent

*   no database mapper that partially hides the database.

    Using an object-relational mapping is not like using an object database.

*   almost no seam between code and database.


## Transactions ##

Make programs easier to reason about.

### Transactions are atomic

Changes made in a transaction are either saved in their entirety or not at all.

This makes error handling a lot easier. If you have an error, you just abort
the current transaction. You don’t have to worry about undoing previous
database changes.


### Transactions affect multiple objects

Most NoSQL databases don’t have transactions. Their notions of consistency are
much weaker, typically applying to single documents. There can be good reasons
to use NoSQL databases for their extreme scalability, but otherwise, think hard
about giving up the benefits of transactions.

ZODB transaction support:

-   ACID transactions with snapshot isolation
-   Distributed transaction support using two-phase commit

    This allows transactions to span multiple ZODB databases and to span ZODB
    and non-ZODB databases.

## Other notable ZODB features

*   Pluggable layered storage

    ZODB has a pluggable storage architecture. This allows a variety of storage
    schemes including memory-based, file-based and distributed (client-server)
    storage. Through storage layering, storage components provide compression,
    encryption, replication and more.

*   Database caching with invalidation

    Every database connection has a cache that is a consistent partial database
    replica. When accessing database objects, data already in the cache is accessed
    without any database interactions. When data are modified, invalidations are
    sent to clients causing cached objects to be invalidated. The next time
    invalidated objects are accessed they’ll be loaded from the database.

    This makes caching extremely efficient, but provides some limit to the number
    of clients. The server has to send an invalidation message to each client for
    each write.

*   Easy testing

    ZODB provides in-memory storage implementations as well as copy-on-write
    layered “demo storage” implementations that make testing database-related code
    very easy.

*   Time travel

    ZODB storages typically add new records on write and remove old records on
    “pack” operations. This allows limited time travel, back to the last pack time.
    This can be very useful for forensic analysis.

*   Binary large objects, Blobs

    Many databases have these, but so does ZODB.

    In applications, Blobs are files, so they can be treated as files in many ways.
    This can be especially useful when serving media. If you use AWS, there’s a
    Blob implementation that stores blobs in S3 and caches them on disk.


### Transactions provide isolation

Transactions allow multiple logical threads (threads or processes) to access
databases and the database prevents the threads from making conflicting
changes.

This allows you to scale your application [link here][1] across multiple
threads, processes or machines without having to use low-level locking
primitives.

You still have to deal with concurrency on some level. For timestamp-based
systems like ZODB, you may have to retry conflicting transactions. With
locking-based systems, you have to deal with possible deadlocks.


[1]: http://slashdot.org
[2]: http://slashdot.org
[link text itself]: http://slashdot.org
