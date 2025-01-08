PlasmidSeq Database
===================

A major component of the pipeline is the Postgres Database that keeps track of the analysis runs. It is unlikely to be
the source of any problems, but will often be a critical tool for troubleshooting.


Schema
------

The database is composed of 5 tables. See the schema below for details on the tables and columns.


.. include:: foundry-datastore-mermaid.rst

Connecting to the database with PyCharm
---------------------------------------

1. Make sure that you have the AWS toolkit plugin installed and configured.
2. In the AWS toolkit widget, find ``Explorer`` -> ``RDS`` -> ``foundry-datastore``.
3. Right click and select ``Connect with Secrets Manager``.
4. From the dropdown box, choose ``foundry-datastore-connection``.
5. Test the connection. You should be all set.


Resetting an Experiment
-----------------------

Sometimes, you need to reset all of :py:class:`~db_model.PlasmidSeqRun` statuses to ``Queued``. The easiest way to
do this is via a SQL command:

.. code-block:: sql

    UPDATE plasmidseqrun
    SET last_step = 'Queued',
        error_type = NULL,
        error_message = NULL,
        error_path = NULL
    WHERE experiment_id = 'THE_NAME_OF_YOUR_RUN';

The usual problem
-----------------

The most common error that can be diagnosed via looking at the database is an error in the template name. The code
provides for a bunch of fixes (like stripping leading and trailing whitespace). But there are always new ways to break
this. You can only edit the template names via the database, so it can be useful there, too.
