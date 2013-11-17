Submit Elasticsearch metrics to Graphite
########################################
:date: 2013-11-17 20:36
:author: smetj
:category: #monitoringlove
:tags: monitoringlove, graphite, metricfactory, metrics, elasticsearch
:slug: submit-elasticsearch-metrics-to-graphite


If you're running an `Elasticsearch`_ cluster you might want to keep track of
the metrics it produces.  In this article I will explain how you can aggregate
the metrics of an Elasticsearch cluster and submit them to Graphite for later
analysis.

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

::

  $ metricfactory list


Elasticsearch
~~~~~~~~~~~~~

Elasticsearch has a HTTP based CRUD API which allows us to poll metrics.
The available metrics resources are:

- http://localhost:9200/_cluster/state
- http://localhost:9200/_stats

Polling these resources returns a JSON formatted document containing metrics
of different Elasticsearch parts.

The `wb_input_httprequest`_ module will help us to fetch those metrics into
our metricfactory setup.

Decode Elasticsearch metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

That JSON document with metrics has to be converted into the Metricfactory
`standard metric format`_.  Once converted it can be processed by other
metricfactory modules.  In this article we will convert the metrics into a
Graphite format using the `Graphite builtin`_ module of Wishbone.


Bootstrapfile
~~~~~~~~~~~~~

Metricfactory needs to be invoked with a bootstrap file which defines the
functionality and eventflow of the server:

.. code-block:: identifier
  :linenos: table

  ---
  modules:
    httprequest_one:
      module: wishbone.input.httprequest
      arguments:
        url: "http://elasticsearch-001:9200/_cluster/nodes/stats"
        interval: 1

    httprequest_two:
      module: wishbone.input.httprequest
      arguments:
        url: "http://elasticsearch-001:9200/_stats"
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
        host: graphite-001
        port: 2013

  routingtable:
    - httprequest_one.outbox  -> funnel.one
    - httprequest_two.outbox  -> funnel.two
    - funnel.outbox           -> decode.inbox
    - decode.outbox           -> encode.inbox
    - encode.outbox           -> output_tcp.inbox
    #- encode.outbox           -> output_screen.inbox
  ...

Lets run over the different sections of this bootstrap file.

The routingtable (line 38) determines how modules are connected to each other
and therefor determine the flow of events.

The *httprequest_one* and *httprequest_two* instances poll the urls (line 6,
12) which return the required metrics.  The pages are requested with an
interval of 1 second (line 7, 13).

The results from both these input modules go over the *funnel* module (line
15) to the *decode* module instance (line 18), where the ES format is
converted to the generic metric format.  The *decode* instance is initialized
using the source argument (line 21) which fills the source value of the
generic metric data format.  This requirement wouldn't be necessary if this
`enhancement request`_ is done.

The decoded events are then converted into the required Graphite format by the
*encode*  module instance (line 23).  This module is initiated with a prefix
argument which puts a prefix (line 26) in front of the metric name.

Events then go to the output_tcp module which submits the metrics into
Graphite itself.

If you want to play around with the metric name formatting, you can write the
metrics to STDOUT first by altering the metric stream to the *output_screen*
modules instance by uncommenting line 44 and commenting line 43.

To start the server, save the above bootstrap configuration to a file and
execute following command:

  $ metricfactory debug --config bootstrap.yaml


.. _Elasticsearch: http://www.elasticsearch.org
.. _Wishbone: https://wishbone.readthedocs.org/en/latest/
.. _Metricfactory: https://github.com/smetj/metricfactory
.. _wb_input_httprequest: https://github.com/smetj/wishboneModules/tree/master/wb_input_httprequest
.. _wb_output_tcp: https://github.com/smetj/wishboneModules/tree/master/wb_output_tcp
.. _document: https://wishbone.readthedocs.org/en/latest/installation.html
.. _standard metric format: http://wishbone.readthedocs.org/en/latest/router.html#format
.. _Graphite builtin: http://wishbone.readthedocs.org/en/latest/modules.html#graphite
.. _enhancement request: https://github.com/elasticsearch/elasticsearch/issues/4179