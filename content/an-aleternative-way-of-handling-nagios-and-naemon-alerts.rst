An alternative way of handling Nagios and Naemon alerts
#######################################################
:date: 2014-03-23 12:00
:author: smetj
:category: #monitoringlove
:tags: monitoringlove, nagios, naemon
:slug: an-aleternative-way-of-handling-nagios-and-naemon-alerts

xxstart_summaryxx

Nagios based monitoring frameworks organize alerting  by associating contacts
to host and service objects.  This is not a very flexible approach and quickly
starts to become a pain to maintain. `Alertmachine`_ is a framework using easy
to understand and flexible alert rules to process alert events outside the
Nagios based monitoring solution.

xxend_summaryxx

The idea is to let the monitoring platform generate rich JSON events every
time a host/service object changes state.  These JSON events contain all
possible metadata about the host/service alert at the moment it is generated.
These events are then processed by *alertmachine* and evaluated against a set
of alert rules.


submit_alert_event
------------------

First, we have to make sure Nagios generates these JSON events.  To make that
work we have to define the `submit_alert_event`_ script as a
*host_notification_command* and *service_notification_command* for each
existing `host and service`_.  Depending on the way you have setup monitoring
it will involve creating a "default" contact and associate it with all hosts
and services.

Using the --json option we can merge all known host/service `macros`_ with the
Livestatus response.  On the `Alertmachine`_ project page you can find an
example on how to do this.


If you're running `mod_gearman`_ then *submit_alert_event* can submit the JSON
events to a queue in Gearmand (see --destination) from which the events can be
consumed by one or more alertmachine processes.  The alternative is to submit
the events over UDP to a alertmachine instance.


Alertmachine
------------

Alertmachine is a `Wishbone`_ based daemon to form an event processing
pipeline consisting out of multiple stages.  The Alertmachine's behaviour is
defined through a Wishbone `bootstrap`_ file.

The bootstrap file might look like this:

.. code-block:: yaml
    :linenos: inline

    ---
    modules:

        input_udp:
            module: wishbone.input.udp
            arguments:
                port: 19283

        input_gearman:
            module: wishbone.input.gearman
            arguments:
                hostlist:
                    - localhost:4730
                secret: somegearmansecret
                queue: alert_event

        funnel:
            module: wishbone.builtin.flow.funnel

        validate:
            module: wishbone.function.json
            arguments:
                mode: decode

        match_engine:
            module: pyseps.sequentialmatch
            arguments:
                location: rules/

        template:
            module: wishbone.function.template
            arguments:
                key: match_engine
                location: templates/
                header_templates:
                    - subject

        email:
            module: wishbone.output.email
            arguments:
                key: match_engine
                mta: localhost:25

        stdout:
            module: wishbone.builtin.output.stdout
            arguments:
                complete: true

    routingtable:
      - input_udp.outbox            -> funnel.one
      - input_gearman.outbox        -> funnel.two
      - funnel.outbox               -> validate.inbox
      - validate.outbox             -> match_engine.inbox
      - match_engine.email          -> template.inbox
      - template.outbox             -> email.inbox
    ...


Input
~~~~~

The *submit_alert_event* script has support to submit events to Alertmachine
via `mod_gearman`_ or directly to a UDP socket.

These inputs are defined by the *input_udp* (line 4) and *input_gearman* (line
7) module instances.


Verification
~~~~~~~~~~~~

To make sure that Alertmachine only processes valid JSON documents we have
initialized the *validate* modules instance (line 13).  It is also responsible
for deserializing the JSON data into a Python data structure (line 16) to
allow further processing.


Event evaluation
~~~~~~~~~~~~~~~~

The `match_engine`_ (line 18) instance is responsible of evaluating any
incoming documents against the `defined rules`_.  These rules are stored in
YAML format in the directory defined by *location* (line 21) and loaded
automatically the moment rules are changed or added.

An example rule looks like this:

.. code-block:: yaml
    :linenos: inline

    ---
    condition:
        alert_type: re:host
        hostgroupnames: in:production
        hostgroupnames: in:noc
        hostgroupnames: in:alert_email
        longdatetime: re:^(Mon|Tue|Wed|Thu|Fri).*

    queue:
        - email:
            from: monitoring@your_company.local
            to:
                - noc@your_company.local
            subject: Alert - Host  {{ hostname }} is  {{ hoststate }}.
            template: host_email_alert
    ...


One file contains 1 rule which on its turn consists out of multiple conditions
(line 2).  If all these conditions match, then the event is submitted to the
defined queues (line 8).  In this example we are forwarding the matching
documents to the module's *email* queue (line 9).  To this queue we have
connected the template module (line 54 bootstrap example) which
effectively forwards the matching JSON events to the *template* module
instance.

The key/value pairs (line 10 to 14) are added to the `header section`_ of all
matching JSON events in order to facilitate the modules which will further
process these events.

Since ultimately we want to send out emails we are adding header information
to the event for the *email* module instance (line 37 bootstrap example) to use.

The available condition are:

+------------+-------------------------+
| Condition  | Function                |
+============+=========================+
| re:        | Regex matching          |
+------------+-------------------------+
| !re:       | Negative regex matching |
+------------+-------------------------+
| >:         | Bigger than             |
+------------+-------------------------+
| >=:        | Bigger or equal to      |
+------------+-------------------------+
| <:         | Smaller than            |
+------------+-------------------------+
| <=:        | Smaller or equal to     |
+------------+-------------------------+
| =:         | Equal to                |
+------------+-------------------------+
| in:        | element in list         |
+------------+-------------------------+

The above example rule will match incoming alert events if the host is member
of the groups production, noc and alert_email and if `longdatetime`_ matches
the defined regex which effectively matches events hapenning on weekdays.


Generating Email alerts
~~~~~~~~~~~~~~~~~~~~~~~

Before sending out any mail, we have to create the content of the message
first.  For this we use the `template`_ module instance (line 30 bootstrap
file). The *template* module expects all templates available in the directory
defined using the *location* variable (line 34).  The template module uses the
Jinja2 templating engine.  The key/value pairs of the JSON alert events can be
used within the template.

The *header_templates* variable (line 35) is a list of header key names which
contain templates that also have to be processed by this module.  In this
particular case, we declare that we have to process the *subject* key since we
have added a template with that name to the header in our alert rule (line 13
evaluation rule).

The module knows which template to use since that has been defined in the
evaluation rule (line 14 evaluation rule).  Make sure the name of the template
to use **exactly** matches the name of the template defined in the evaluation
rule (line 14).

Once the template has been made, the event has been converted from a JSON
document into the content defined by the template.


Sending email
~~~~~~~~~~~~~

The `email`_ module instance knows where to send the incoming events since it
expects to find the subject, from and to values stored in the event header
under the defined key (line 41 boostrap).  The *match_engine* instance writes
these values to the header as defined in the evaluation rule (line 10-13
evaluation rule).  The email is then send via the defined MTA (line 42
bootstrap file).


Starting and testing Alertmachine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given that you have defined the locations of the *rules* and *templates* and
that you have set the correct email addresses in the alert rules, you should
be able to start Alertmachine like this:

    $ wishbone debug --config /etc/alertmachine.yaml

To execute a test we can submit a `test event`_ to the Alertmachine's UDP
socket:

    $ cat sample.json|nc -u localhost 19283


If you want to send the email events to STDOUT instead of actually sending
them to your defined MTA, you should connect *template.outbox* to
*email.inbox* (line 55 bootstrap file).


Final words
~~~~~~~~~~~

Using the Alertmachine setup we have a flexible and powerful alerting platform
for your Nagios/Naemon based monitoring system which can be easily integrated
without much change to your monitoring configuration.

For now, alerts are only send out via email.  There are however more `output
modules`_ available.  If there are any missing, these can be developed and
added with relative ease.

.. [1] `This article has been altered for correctness`_


.. _Alertmachine: https://github.com/smetj/alertmachine
.. _macros: http://nagios.sourceforge.net/docs/3_0/macrolist.html
.. _submit_alert_event: https://github.com/smetj/alertmachine/tree/master/alertmachine/submit_alert_event
.. _host and service: http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html#contact
.. _mod_gearman: https://labs.consol.de/nagios/mod-gearman
.. _wishbone: https://wishbone.readthedocs.org/en/latest/
.. _bootstrap: https://wishbone.readthedocs.org/en/latest/index.html#bootstrapping
.. _defined rules: https://github.com/smetj/alertmachine/blob/master/alertmachine/rules/000-host-alert.yaml
.. _header section: https://wishbone.readthedocs.org/en/latest/patterns.html#event-headers
.. _match_engine: https://pypi.python.org/pypi/pyseps
.. _template: https://pypi.python.org/pypi/wb_function_template
.. _jinja2: http://jinja.pocoo.org/docs
.. _longdatetime: http://nagios.sourceforge.net/docs/3_0/macrolist.html#longdatetime
.. _email: https://pypi.python.org/pypi/wb_output_email
.. _test event: https://github.com/smetj/alertmachine/blob/master/alertmachine/sample_json_alert_event/sample.json
.. _output modules: https://github.com/smetj/wishboneModules
.. _This article has been altered for correctness: https://github.com/smetj/smetj.net/commits/master/content/an-aleternative-way-of-handling-nagios-and-naemon-alerts.rst