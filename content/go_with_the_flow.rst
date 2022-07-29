Go with the flow: Wishbone flow modules
#######################################
:date: 2016-04-17 16:30
:author: smetj
:category: technology
:slug: go_with_the_flow



`Wishbone`_ servers are all about event flow flexibility.  In this article we
will cover the role of the different built-in *flow* modules and how to shape
the flow of events along with some practical examples.




.. contents:: Table of Contents
   :depth: 2

What are flow modules?
----------------------

Wishbone module queues can only have one direct connection to another module's
queue. It's not possible to connect multiple queues directly to each other.

To setup advanced event routing logic, Wishbone includes the *flow module
category* containing modules which decide the path events follow whilst
traveling through the server from one module to the other.

Flow modules do not alter the content of events but merely shovel them between
the connected module queues based on the routing logic properties of the flow
module itself.

This blog post discusses each of the built-in flow modules including a minimal
practical example to illustrate the possibilities [ref] Some of the examples
require `external Wishbone modules`_ to be installed. [/ref]

Examples
--------

Fanout
~~~~~~

The fanout message pattern done by the `wishbone.flow.fanout`_ is a well known
messaging pattern.  Incoming events are simply duplicated to each outgoing queue.

Example use case
++++++++++++++++

A TCP server which accepts, duplicates and forwards the received events to 3 separate TCP
servers in different availability zones:

[gist:id=718879806ed24d1782c39e88b6d5e7b9,file=bootstrap.yaml]


Funnel
~~~~~~

The funnel message pattern is the inverse of the *fanout* pattern and is
handled by the `wishbone.flow.funnel`_ module. Events of multiple incoming
queues are forwarded to 1 outgoing queue.

Example use case
++++++++++++++++

A TCP server which receives JSON as well as MSGPack data and indexes that into
Elasticsearch.

[gist:id=d8f98e3dad07ca7ed4347cfa8360dfeb,file=bootstrap.yaml]


Fresh
~~~~~

The `wishbone.flow.fresh`_ module shovels incoming events from the *inbox*
queue to the *outbox* queue without modifying them.  If however no data has
been submitted to the inbox queue in the last x seconds, a *new event* with a
custom payload is generated and submitted into the *timeout* queue for another
module to process.  When the event stream recovers another event with a custom
*recovery* payload is generated and submitted to the *timeout* queue.

This module is practical to trigger some process one way or the other when no
data arrives into the Wishbone server for a configurable amount of time.


Example use case
++++++++++++++++

A server which accepts JSON data over http and validates data against JSON
schema [ref]An external flow module to validate JSON data against a JSON
schema https://github.com/smetj/wishbone-flow-jsonvalidate [/ref] prior to
forwarding it to RabbitMQ for further processing.  We know the incoming stream
of data is continuous, if not something is wrong and we want to send an alert
event to Pagerduty.

[gist:id=382b3b3314e6dd309d9af73a1e11ab27,file=bootstrap.yaml]


Roundrobin
~~~~~~~~~~

The `wishbone.flow.roundrobin`_  module pretty much does what it says. It
takes events from its *inbox* queue and forwards them in a round robin fashion
to the connected modules.

Example use case
++++++++++++++++

A server which collects metrics from Elasticsearch and submits them to a set
of Graphite relay nodes in order to spread the load equally over them.

[gist:id=fbc9c5a906328587fadf47bf3b8d5307,file=bootstrap.yaml]


Switch
~~~~~~

The `wishbone.flow.switch`_ module can reroute the incoming events from one
queue to another connected queue by dynamically setting the destination using
a `lookup value`_ or by submitting a message to the module's *switch* queue.

Example use case
++++++++++++++++

Temporarily redirect incoming webhook events from one RabbitMQ server to
another.

[gist:id=fbe7313bbf01245fbe365df7d5be5d08,file=bootstrap.yaml]


By default incoming events are routed to the *rabbitmq-001.az1.company.local*
RabbitMQ instance.

Switching to the other backend would involve submitting an event with the
queue name to the */switch* endpoint of the *input* module:


.. code-block:: bash

    $  echo backend_az_2|curl -d @- http://localhost:19283/switch


Tippingbucket
~~~~~~~~~~~~~

The `wishbone.flow.tippingbucket`_ module buffers incoming events and flushes
the buffered events as a `bulk event`_ to the next module.

Example use case
++++++++++++++++

Instead of submitting one metric at a time to Graphite it's much more
efficient to submit multiple metrics at once and hereby limit the number of
TCP connects.

We extend the `roundrobin`_ example to submit 500 metrics at once to each
Graphite relay server.


[gist:id=fbe7313bbf01245fbe365df7d5be5d08,file=bootstrap.yaml]


Final words
-----------

We have covered the built-in Wishbone flow modules in this article along with
some examples clarifying the use case of each of them so it might inspire you
to create a setup suited for your specific use case.

Please go ahead and give Wishbone a try and I'd greatly welcome feedback and ideas.


Footnotes:

.. _Wishbone: http://wishbone.readthedocs.org/en/latest
.. _wishbone.flow.fanout: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-fanout
.. _wishbone.flow.funnel: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-funnel
.. _wishbone.flow.fresh: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-fresh
.. _wishbone.flow.roundrobin: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-roundrobin
.. _wishbone.flow.switch: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-switch
.. _wishbone.flow.tippingbucket: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-tippingbucket
.. _lookup value: http://wishbone.readthedocs.org/en/latest/server/lookup%20functions.html
.. _bulk event: http://wishbone.readthedocs.org/en/latest/modules/bulk%20events.html
.. _roundrobin: ./go_with_the_flow.html#roundrobin
.. _external Wishbone modules: http://wishbone.readthedocs.org/en/latest/modules/external%20modules.html
