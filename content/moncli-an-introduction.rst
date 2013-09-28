Moncli - An introduction
########################
:date: 2012-02-09 00:20
:author: smetj
:category: monitoring
:tags: moncli, monitoringlove, rabbitmq
:slug: moncli-an-introduction

|image0|

One of the classic tasks one has to deal with when working with a
monitoring framework is have the ability to retrieve metrics from an OS
or server which aren't available just like that over the network. There
are plenty of different techniques and a multitude of clients available
which offer this functionality.  Covering them falls out of the scope of
this post.

So why another Monitoring Client?
---------------------------------

When running into scalability problems with my Nagios setup, I realized
that the reason for this is the fact that Nagios always has to take the
initiative to poll a client.  This is in Nagios terminology called an
active check.  It's of course normal that a client receives instructions
on what it needs to do like which plugin to execute or which thresholds
to evaluate.  However, if you think about it, why do we have to repeat
the same question over and over again while in essence nothing has ever
changed between the current and the previous request? Isn't it normal we
ask a question once and say report back at this interval and carry on
until further notice?

So why not offloading all (or most of) the scheduling effort a central
monitoring system has to perform to the monitoring clients running on
your hosts?

If you would take it further, you could turn each of my monitoring
clients into an "independent miniature monitoring engine".  This way you
could shift the load from a central system to the collective of clients
in the network.  This basically results in horizontal scalability and a
decentralized setup.

Requirements
------------

Open and rich data format
~~~~~~~~~~~~~~~~~~~~~~~~~

All in- and outgoing communication should be done in an clear and open
data format, which offers the flexibility to transform it into any
other desirable format which allows you to integrate the client with an
existing platform but which in its turn also allows you to move away
from it.  All `incoming`_ to and `outgoing`_ data from Moncli is in JSON
format. This makes sure that Moncli data is manipulated easily.

Scheduling
~~~~~~~~~~

As said, the client needs to be able to schedule a request at an
`interval of choice`_. When the client restarts, it should remember its
scheduled requests and carry on from the moment it's alive again. Moncli
has a build in scheduler which `writes its schedule to disk`_.

Flexible messaging.
~~~~~~~~~~~~~~~~~~~

Since Moncli has its own scheduler, it has to submit the check results
somehow in a trustworthy way without actually having to care much about
who consumes the data when and where. Moncli submits check results into
the `RabbitMQ`_ message broker, which offers a great deal of
flexibility.

Moncli `listens`_ on the message broker infrastructure for incoming
requests. Each Moncli client registers a queue using its FQDN as a name
on the message broker infrastructure from where it receives the requests
it should execute.

Simple, manageable but safe plugin design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Metrics have to come from somewhere. When Moncli executes a request, it
actually executes a locally stored plugin. `All this plugin needs to do
is create a list of key/value pairs`_. This significantly lowers the
difficulty and time required to create new plugins which also allows
less experienced people to write plugins. Moncli will only execute
`locally stored plugins`_ which have a hash which matches the one in the
request. When a plugin with such a hash isn't found locally, it will try
to download an update or new version from `a central location`_.

Evaluation of metrics
~~~~~~~~~~~~~~~~~~~~~

Nagios plugins require you to build in the evaluation of thresholds in
them by feeding the plugin the warning and critical values.  Moncli also
performs the evaluation of metrics on the client side but takes another
approach.  Instead of doing threshold evaluation in the plugin, Moncli
does the evaluation itself, based upon the `thresholds`_ one provides in
combination with a an evaluator.

There are currently 2 `types of evaluators`_ (more planned):

Formulas: calculations using the keys/values returned by the plugin.
Regexes: Simple regex matching on the output of a plugin (not key
value pairs)

It's optional to define evaluators in a request.  In this case, Moncli
just becomes a metrics collector.

A good starting point to figure out what the possibilities of Moncli are
is done by looking through  the in- and outgoing data format of Moncli
called `requests`_ and `reports`_.

A second post will be about consuming and processing of Moncli data from
RabbitMQ.

.. _incoming: http://wiki.smetj.net/wiki/Moncli_documentation#Request
.. _outgoing: http://wiki.smetj.net/wiki/Moncli_documentation#Reports
.. _interval of choice: http://wiki.smetj.net/wiki/Moncli_documentation#cycle
.. _writes its schedule to disk: http://wiki.smetj.net/wiki/Moncli_documentation#cache
.. _RabbitMQ: http://www.rabbitmq.com/
.. _listens: http://wiki.smetj.net/wiki/Moncli_documentation#Communication
.. _All this plugin needs to do is create a list of key/value pairs: http://wiki.smetj.net/wiki/Moncli_documentation#Plugins
.. _locally stored plugins: http://wiki.smetj.net/wiki/Moncli_documentation#local_repo
.. _a central location: http://wiki.smetj.net/wiki/Moncli_documentation#remote_repo
.. _thresholds: http://wiki.smetj.net/wiki/Moncli_documentation#thresholds
.. _types of evaluators: http://wiki.smetj.net/wiki/Moncli_documentation#Evaluator_definitions
.. _requests: http://wiki.smetj.net/wiki/Moncli_documentation#Request
.. _reports: http://wiki.smetj.net/wiki/Moncli_documentation#Reports

.. |image0| image:: http://smetj.net/wp-content/uploads/2012/02/Moncli_architecture_11-300x231.jpg
   :target: http://smetj.net/2012/02/09/moncli-an-introduction/moncli_architecture_1-2/
