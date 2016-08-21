Quis custodiet ipsos custodes: Monitoring a poll-based monitoring solution
##########################################################################
:date: 2016-04-18 23:30
:author: smetj
:category: monitoring
:tags: wishbone, devops, monitoringlove, pagerduty
:slug: monitoring_a_poll-based_monitoring_solution

__start_summary__

Your monitoring platform is susceptible to failure pretty much like any other
component within your infrastructure. Having your monitoring monitored is a
topic you should consider spending some time on.  In this article we will
cover how you can use Wishbone to cross check your monitoring setup and alert
an external service such as Pagerduty in case of downtime.

__end_summary__

----

A poll-based architecture
-------------------------

Poll-based monitoring is (arguably) the most common monitoring architecture.
Polling means the initiative of validating the state of some endpoint lies
with a central scheduler which repeatedly executes a check to determine the
state of that endpoint.

*Icinga, Nagios, Shinken, Naemon* and *OP5* are all examples of monitoring
solutions relying on some form of a central scheduler executing checks.
[ref]These frameworks are also able to process passive checks which are status
updates submitted by an external process. [/ref]


The plan
--------

A good start is to have an *external monitoring application* validating
whether checks are actually being *scheduled and executed* on the *monitoring
application*.  On top of that, we also want to know whether the *"external
monitoring application"* itself is functioning properly.

.. highlights::

    It's **important** to construct the setup in such a way that both
    applications cross-monitor one another.


If the *monitoring application* is able to successfully POST every minute,
data over http (`check_http`_) to the *external monitoring application* it
knows the *external monitoring application* is up and running.  If that's not
the case then the *monitoring application* should alert accordingly.

If the *external monitoring application* does not receive at least 1 POST
event over http (`check_http`_) in 2 minutes, it knows the monitoring
application is not scheduling and executing checks and therefor generate an
alert.


Wishbone
--------

We can use `Wishbone`_ to construct an *external monitoring application* which
expects to receive data every 2 minutes via http POST.

2 key Wishbone modules to achieve this are:

- `wishbone.input.httpserver`_
- `wishbone.flow.fresh`_


Bootstrapping the server
++++++++++++++++++++++++

To install Wishbone including the external modules required for this setup
execute: [ref]External modules are separate projects not included with
Wishbone [/ref]

.. code-block:: bash

    $ pip install wishbone wishbone-input-httpserver wishbone-output-http


The bootstrap file:

[gist:id=444f981d39f5897741ecc33788f1f3f5,file=bootstrap.yaml]


Running the server is really simple:

.. code-block:: bash

    $ wishbone start --config bootstrap.yaml


check_http command
++++++++++++++++++

The `check_http`_ command scheduled and executed every minute by the
*monitoring application* should be doing something similar to:

.. code-block:: bash

    $ /usr/lib64/nagios/plugins/check_http -H wishbone-server-001.company.local -p 19283 -P hello


Final words
-----------

Using this setup we have achieved the the desired setup of 2 applications
monitoring each other's availability. In case the Wishbone server goes down
the *monitoring application* itself will alert.  In case the *monitoring
application* is down Wishbone will not receive any incoming data and therefor
trigger a Pagerduty alert. [ref]Depending on your needs, Wishbone offers other
ways to generate alerts. [/ref]

The described setup will not cover all possible failure scenario's although it
is a first good step to have your monitoring setup monitored.

Please go ahead and give Wishbone a try and I'd greatly welcome feedback and
ideas.


Footnotes:

.. _Wishbone: http://wishbone.readthedocs.org/en/latest
.. _check_http: https://www.monitoring-plugins.org/doc/man/check_http.html
.. _Pagerduty: http://www.pagerduty.com
.. _wishbone.flow.fresh: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-fresh
.. _wishbone.input.httpserver: https://pypi.python.org/pypi?name=wishbone_input_httpserver&:action=display

