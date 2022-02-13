Exceptions as a feature
#######################
:date: 2014-09-16 21:00
:author: smetj
:category: development
:tags: python, wishbone
:slug: exceptions_as_a_feature

..start_summary..

`Wishbone`_ `modules`_ process and transport messages in one way or the other.
Obviously, this needs to happen as reliable as possible.  `Wishbone`_ has a
particular way of dealing with `exceptions`_.  In this article we cover the
role unhandled code `exceptions`_ can play and how we can take advantage of
them by  just allowing them to happen.

..end_summary..

Failed and successful queues
----------------------------

Messages travel between modules via queues.  By default, a module has an
*inbox*, *successful* and *failed* queue. Typically, a module has a function
`registered`_ against the *inbox* queue.  This function will then process each
message from the associated queue.  After the function successfully processes
the message it will be automatically submitted to the module's *successful*
queue.  On the contrary, whenever the function generates an exception while
processing the message, it will be submitted to the *failed* queue.

If a queue is not connected to another queue it will drop the messages it
receives.  So by connecting another module to the failed queue, we can forward
the offending messages to another module in order to construct a failover
strategy.  Therefor it is important not to trap any `exceptions`_ inside the
*registered function* which allows the `Wishbone`_ framework to submit the
message to the module's *failed* queue.


The TCPOut module
-----------------

The `wishbone.output.tcp`_ module submits messages to a TCP socket. The
consume function has been `registered to consume`_ all messages from the inbox
queue.

There is no error handling code inside this function.  If submitting a message
to the `socket`_ fails an exception will be raised.  Whenever that's the case,
the the message will be submitted to the module's *failed* queue.


A failover strategy
-------------------

The described behavior can be demonstrated with a test setup using following
`bootstrap`_ file:

.. code-block:: YAML
  :linenos:

    ---
    modules:

      dictgenerator:
        module: wishbone.input.dictgenerator
        arguments:
          interval: 0.5

      output_1:
        module: wishbone.output.tcp
        arguments:
          port: 10001

      output_2:
        module: wishbone.output.tcp
        arguments:
          port: 10002

      output_3:
        module: wishbone.output.tcp
        arguments:
          port: 10003

      diskout:
        module: wishbone.output.disk
        arguments:
          directory: ./buffer

      diskin:
        module: wishbone.input.disk
        arguments:
          directory: ./buffer
          idle_trigger: true
          idle_time: 20

      funnel:
        module: wishbone.flow.funnel

    routingtable:
      - dictgenerator.outbox  -> funnel.one
      - funnel.outbox         -> output_1.inbox
      - output_1.failed       -> output_2.inbox
      - output_2.failed       -> output_3.inbox
      - output_3.failed       -> diskout.inbox
      - diskin.outbox         -> funnel.two
    ...


This `bootstrap`_ file creates a `Wishbone`_ server which generates a random
dictionary every half a second.  This dictionary is submitted to the
**output_1** module instance which will try to submit the message to
*localhost tcp/10001*. If this fails then the message will be forwarded to
module instance **output_2** which tries to submit the message to
*tcp/10002*. When that fails then the message will be forwarded to the module
instance **output_3** which tries to submit the message to *tcp/10003*.
Whenever the third destination fails then there message is forwarded to the disk
buffer module, which feeds back into the TCP destinations in order to retry
submitting the messages again to one of the TCP destinations.


To `start`_ `Wishbone`_ execute following command [1]_:

::

    $ wishbone debug --config failovertest.yaml



In three separate terminals start following `socat`_ instances:


::

    $ socat tcp4-listen:10001,fork stdout


::

    $ socat tcp4-listen:10002,fork stdout


::

    $ socat tcp4-listen:10003,fork stdout


At this point, messages should be arriving to the socat instance listening on
port 10001.  Interrupting that socat instance makes the messages arrive to the
instance listening on port 10002.  When the first socat instance is restored
then the messages should be arriving back there again.  If all three TCP
destination are unavailable then the messages are submitted to a disk buffer.
You should see `Wishbone`_ log error messages when submitting data to a TCP
destination fails.


Final words
-----------

By chaining the failed queues into a sequential list of destinations it's
fairly easy to create a fail-over strategy in a `Wishbone`_ setup.  Questions
and suggestions always welcome!

.. [1] There is a Wishbone `Docker container`_ available.

.. _Wishbone: http://wishbone.readthedocs.org/en/latest/
.. _modules: http://wishbone.readthedocs.org/en/latest/wishbone%20module.html
.. _registered: http://wishbone.readthedocs.org/en/latest/components.html#wishbone.Actor.registerConsumer
.. _wishbone.output.tcp: http://wishbone.readthedocs.org/en/latest/builtin%20modules.html#wishbone-output-tcp
.. _consume: https://github.com/smetj/wishbone/blob/master/wishbone/module/tcpout.py#L109
.. _socket: https://github.com/smetj/wishbone/blob/master/wishbone/module/tcpout.py#L114
.. _registered to consume: https://github.com/smetj/wishbone/blob/master/wishbone/module/tcpout.py#L73
.. _bootstrap: http://wishbone.readthedocs.org/en/latest/bootstrap.html
.. _start: http://wishbone.readthedocs.org/en/latest/bootstrap.html#start
.. _Docker container: http://wishbone.readthedocs.org/en/latest/installation.html#docker
.. _exceptions: https://docs.python.org/2/tutorial/errors.html
.. _socat: http://www.dest-unreach.org/socat