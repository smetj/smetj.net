Submit Elasticsearch metrics to Graphite
########################################
:date: 2013-11-17 20:36
:author: smetj
:category: #monitoringlove
:tags: monitoringlove, graphite, metricfactory, metrics, elasticsearch
:slug: submit-elasticsearch-metrics-to-graphite


If you're running an `Elasticsearch`_ cluster you might want to keep track of
the metrics it produces.  In this article I explain how you can aggregate the
metrics of an Elasticsearch cluster and submit them to Graphite. [1]_

xxend_summaryxx

Prerequisites
~~~~~~~~~~~~~

You need to have following software installed:

Main software (installable from Pypi)

- `Metricfactory`_

Additional modules (Install from source)

- `wb_input_httprequest`_
- `wb_output_tcp`_


This `document`_ describes how to install the different aspects of Wishbone
and its modules.

Once installed you should have the *metricfactory* executable available.
You can test this by issuing following command:

::

  $ metricfactory list --group metricfactory.decoder


Elasticsearch
~~~~~~~~~~~~~

Elasticsearch has a HTTP based API which allows us to poll metrics.
The available metrics resources are:

- `Cluster stats`_
- `Nodes stats`_
- `Indices stats`_

Polling these resources returns a JSON formatted document containing metrics
of different Elasticsearch parts.

The `wb_input_httprequest`_ module allows us to poll and collect these
resources.

Decode Elasticsearch metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The returned JSON document containing metrics has to be converted into the
Metricfactory `standard metric format`_.  Once converted they can be processed
by other Metricfactory modules.  We will convert the metrics into the Graphite
format using the `Graphite builtin`_ module of Wishbone.


Bootstrapfile
~~~~~~~~~~~~~

Metricfactory requires a bootstrap file which defines the functionality and
eventflow:

.. code-block:: identifier
  :linenos: table

  ---
  modules:
    httprequest_one:
      module: wishbone.input.httprequest
      arguments:
        url: "http://elasticsearch-node-001:9200/_cluster/stats"
        interval: 1

    httprequest_two:
      module: wishbone.input.httprequest
      arguments:
        url: "http://elasticsearch-node-001:9200/_nodes/stats"
        interval: 1

    httprequest_three:
      module: wishbone.input.httprequest
      arguments:
        url: "http://elasticsearch-node-001:9200/_stats"
        interval: 1

    funnel:
      module: wishbone.builtin.flow.funnel

    decode:
      module: metricfactory.decoder.elasticsearch
      arguments:
        source: lhi

    encode:
      module: wishbone.builtin.metrics.graphite
      arguments:
        prefix: application.elasticsearch.
        script: false

    output_screen:
      module: wishbone.builtin.output.stdout

    output_tcp:
      module: wishbone.output.tcp
      arguments:
        host: localhost
        port: 2013

  routingtable:
    - httprequest_one.outbox   -> funnel.one
    - httprequest_two.outbox   -> funnel.two
    - httprequest_three.outbox -> funnel.three
    - funnel.outbox            -> decode.inbox
    - decode.outbox            -> encode.inbox
    - encode.outbox            -> output_tcp.inbox
  ...

Lets run over the different sections of this bootstrap file.

The routingtable (line 44) determines how modules are connected to each other
and therefor determine the flow of events.

The *httprequest_one*, *httprequest_two* and *httprequest_three* instances
poll the urls (line 6, 12 and 18) which return the available metrics in JSON
format.  The resources are requested with an interval of 1 second (line 7, 13,
19).

The results coming out these 3 input modules then flow via the *funnel* module
(line 21) into the *decode* module (line 24) in which the JSON formatted data
is converted to the generic metric format.  The *decode* instance is
initialized using the source argument (line 27) which allows you to add the
cluster name to the metric names in case you're collecting metrics from
multiple cluster instances.

The decoded events are then converted into the required Graphite format by the
*encode*  module instance (line 29).  The prefix argument (line 32) allows you
to define the top scope of the metric names.

Events then go to the output_tcp module which submits the metrics into
Graphite itself.

If you first want to experiment with the metric name formatting, you can write
the metrics to STDOUT by connecting *encode.outbox* to *output_screen.inbox*
(line 50).

To start the server, save the above bootstrap configuration to a file and
execute following command:

  $ metricfactory debug --config bootstrap.yaml

.. [1] `This article has been altered for correctness`_

.. _Elasticsearch: http://www.elasticsearch.org
.. _Wishbone: https://wishbone.readthedocs.org/en/latest/
.. _Metricfactory: https://github.com/smetj/metricfactory
.. _wb_input_httprequest: https://github.com/smetj/wishboneModules/tree/master/wb_input_httprequest
.. _wb_output_tcp: https://github.com/smetj/wishboneModules/tree/master/wb_output_tcp
.. _document: https://wishbone.readthedocs.org/en/latest/installation.html
.. _standard metric format: http://wishbone.readthedocs.org/en/latest/router.html#format
.. _Graphite builtin: http://wishbone.readthedocs.org/en/latest/modules.html#graphite
.. _enhancement request: https://github.com/elasticsearch/elasticsearch/issues/4179
.. _Indices stats: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-stats.html
.. _Cluster stats: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-stats.html
.. _Nodes stats: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
.. _This article has been altered for correctness: https://github.com/smetj/smetj.net/commits/master/content/submit-elasticsearch-metrics-to-graphite.rst