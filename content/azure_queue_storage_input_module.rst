Azure Queue Storage input module
################################
:date: 2018-03-18 15:00
:author: smetj
:category: development
:tags: wishbone, release, module, azure
:slug: azure_queue_storage_input_module

.. role:: text(code)
   :language: text

__start_summary__

I have just released the first version of :text:`wishbone-input-azure_queue_storage`
a Wishbone input module to consume messages from Microsoft's `Azure Queue Storage`_ service.

In this article we will run through a "Hello world" example illustrating its usage.

__end_summary__


----


Goal
----

In this article I will demonstrate how to consume messages from the `Azure
Queue Storage` using the newly released
`wishbone_contrib.module.input.azure_queue_storage`_ module and print it to STDOUT.


Boostrap file
-------------

The Wishbone boostrap we will be using looks similar to this:

.. code-block:: yaml

    protocols:
      json:
        protocol: wishbone.protocol.decode.json

    modules:
      input:
        module: wishbone_contrib.module.input.azure-queue-storage
        arguments:
          account_name: ABC
          account_key: XYZ
          auto_message_delete: True

      output:
        module: wishbone.module.output.stdout
        arguments:
          selection: null

    routingtable:
      - input.outbox -> output.inbox

You will have to make sure you complete the bootstrap file with the correct
values for :text:`account_name` and :text:`account_key`.


Boostrapping the server
-----------------------

We will use the Docker container to bootstrap our server:

.. code-block:: text

    $ docker run -t -i --privileged -v $(pwd)/bootstrap.yaml:/bootstrap.yaml \
        docker.io/smetj/wishbone-input-azure_queue_storage:latest start --config /bootstrap.yaml
    Instance started in foreground with pid 1
    2018-03-18T14:09:19.6830+00:00 wishbone[1] informational input: Connected to Azure Queue Service https://xxxxxx.queue.core.windows.net/wishbone



Sending a message
-----------------

We will use the Azure console to manually send a message. As you can see at
this point the :text:`wishbone` has already been created.

|azure_1|


On the server side we should see following output:

.. code-block:: text

    {'cloned': False, 'bulk': False, 'data': 'Hello from the Azure Queue Storage service!', 'errors': {}, 'tags': [], 'timestamp': 1521382660.3213623, 'tmp': {'input': {'id': '79afcb44-b546-4e63-afc3-8190e5c7ae77', 'insertion_time': '1521382660', 'expiration_time': '1521987460', 'dequeue_count': 1, 'pop_receipt': 'AgAAAAMAAAAAAAAADDPH4MO+0wE=', 'time_next_visible': '1521382662'}, 'output': {}}, 'ttl': 253, 'uuid_previous': [], 'uuid': 'c8c2d273-6063-4b6d-9c90-6d603169a2fd'}


The message has been permanently deleted from the queue because of the
:text:`auto_message_delete` option. If we want to delete the message from the
queue after it has been processed successfully (printing to STDOUT in this
demo) we can slightly change our setup.


Delete message after successful processing
------------------------------------------

For this we will make use of Wishbone module's default :text:`_success` queue
and the :text:`delete` queue of :text:`wishbone_contrib.module.input.azure-
queue-storage`.

Messages ending up in the :text:`delete` queue will be processed by the module
to be deleted from the Azure queue.

.. code-block:: yaml

    modules:
      input:
        module: wishbone_contrib.module.input.azure-queue-storage
        arguments:
          account_name: ABC
          account_key: XYZ
          visibility_timeout: 2
          auto_message_delete: False

      output:
        module: wishbone.module.output.stdout
        arguments:
          selection: null

    routingtable:
      - input.outbox     -> output.inbox
      - output._success -> input.delete

For this setup to work, we set :text:`visibility_timeout` to 2 seconds to
indicate the message should reappear for other consumers to consume when our
setup fails to process the said message properly.


Conslusion
----------

This initial version of `wishbone_contrib.module.input.azure_queue_storage`_
allows us to consume messages from Azure queue storage with ease. The module is
an initial version which doesn't support yet all features the queueing service
offers.

The `Wishbone`_ support for the `Azure Queue Storage`_ service allows you to
develop servers which consume and process messages in no-time!

Obviously, you will need to have the possibility to submit messages too, but
that will be a new module and the next small project I'll be working on.

If you have any questions, remarks or suggestions please feel free getting in touch.


.. _Azure Queue Storage: https://azure.microsoft.com/en-us/services/storage/queues/
.. _wishbone_contrib.module.input.azure_queue_storage: https://github.com/wishbone-modules/wishbone-input-azure_queue_storage
.. _Wishbone: http://wishbone.readthedocs.io
.. |azure_1| image:: pics/azure_queue_storage_1.png
