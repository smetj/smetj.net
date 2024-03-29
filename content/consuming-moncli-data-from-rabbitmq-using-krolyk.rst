Consuming Moncli data from RabbitMQ using Krolyk
################################################
:date: 2012-02-11 18:08
:author: smetj
:category: technology
:slug: consuming-moncli-data-from-rabbitmq-using-krolyk

What's in a name?
~~~~~~~~~~~~~~~~~

Before we go into more detail on how to execute plugins,
manipulate and evaluate data with Moncli we first have to take a look
how we are going to consume the data produced by Moncli from RabbitMQ.
 I found myself quite often in the situation where I had to write again
and again a daemon or process which consumes data from RabbitMQ and do
something with it.  I already started to write `Krolyk`_ which initial
goal was to consume Nagios passive check results from RabbitMQ and write
them into the Nagios command pipe.  I found that too specific, so I
changed Krolyk into a more `modular or plugin system`_, which allows you
to write a `simple Python class`_ which consumes data from RabbitMQ.
 The nice thing about it is when you write a plugin for Krolyk, it will
start one or more  parallel consumers without you having to worry about
how to organize all that.  This makes writing consumers for RabbitMQ
easy and accessible to more people.  Krolyk's use is however \ **not**\
limited to the monitoring and metrics collection scope.  It's intended
to be generic, allowing one to easily write parallel RabbitMQ consumers.

Consuming Moncli data from RabbitMQ

So let's setup Krolyk to consume and simply display data produced by
Moncli.

To realize this we can use the `skeleton.py`_ plugin.  The *skeleton*
plugin can be used as a base for your new and more complex plugins.
 What skeleton does out of the box is just print the content it consumes
from the broker to stdout and acknowledge it back to the broker so it's
removed from the queue.  Just have a look at the *consume* function.
 This should pretty much give you an idea of what you can do with it.

Configuration
~~~~~~~~~~~~~

Krolyk has a config file in which you can define parameters to connect
to RabbitMQ and parameters which are available to the plugin you write.
 If we take a look at krolyk.cfg we can see under the ["plugins"]
section a configuration section for each individual plugin.  You have to
make sure that the name of the plugin section is exactly the same
(including case) as the name of your class.

::

    [ccnbw_ini width="500" lines="-1" ]
    [ "plugins" ]
        [[ "Skeleton" ]]
            "_enabled"       = False
            "_workers"       = 5
            "_broker"        = "sandbox"
            "_queue"         = "moncli_reports"
            "_user"          = "guest"
            "_password"      = "guest"
            "blah1"          = "whatever"
            "fu"             = "bar"
    [/ccnbw_ini]

Each plugin/class should have at minimal the parameters defined required
to  connect to the RabbitMQ broker.  These parameters all start with an
underscore.  All other variables you define will be available to your
class as a dictionary called "self.configuration"

A practical example
~~~~~~~~~~~~~~~~~~~

So let's start an instance of Krolyk which consumes data produced by
Moncli and prints it to stdout.  Keep in mind Krolyk that if the queue
doesn't exist, Krolyk will create a durable one for you.

#. Start Krolyk in the foreground with a config file which works for
   your environment:

   ::

       jelle@indigo:~$ /opt/krolyk/bin/krolyk debug --config /opt/krolyk/etc/krolyk.cfg

#. Submit a test string to the AMQP default exchange:\ |image1|
#. And see it appear on the command line:\ |image2|

This example isn't really doing anything exciting but, I at least it
gives you an idea on what functionality Krolyk offers.  Using the
information from this post you should be able to display the data
generated by Moncli, so you have an idea what comes out of it.

In the next post we will be creating Requests and Reports with Moncli.

.. _Krolyk: https://github.com/smetj/krolyk
.. _modular or plugin system: https://github.com/smetj/krolyk/tree/master/lib/plugins
.. _simple Python class: https://github.com/smetj/krolyk/blob/master/lib/plugins/skeleton.py
.. _skeleton.py: https://github.com/smetj/krolyk/blob/master/lib/plugins/skeleton.py

.. |image0| image:: http://smetj.net/wp-content/uploads/2012/02/Krolyk-300x185.jpg
   :target: http://smetj.net/2012/02/11/consuming-moncli-data-from-rabbitmq-using-krolyk/krolyk-2/
.. |image1| image:: http://smetj.net/wp-content/uploads/2012/02/krolyk_rabbit1-150x150.jpg
   :target: http://smetj.net/2012/02/11/consuming-moncli-data-from-rabbitmq-using-krolyk/krolyk_rabbit1/
.. |image2| image:: http://smetj.net/wp-content/uploads/2012/02/krolyk_rabbit2-300x91.jpg
   :target: http://smetj.net/2012/02/11/consuming-moncli-data-from-rabbitmq-using-krolyk/krolyk_rabbit2/
