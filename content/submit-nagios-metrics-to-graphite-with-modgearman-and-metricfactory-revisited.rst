Submit Nagios metrics to Graphite with ModGearman and MetricFactory revisited
#############################################################################
:date: 2013-11-06 22:00
:author: smetj
:category: #monitoringlove
:tags: monitoringlove, graphite, metricfactory, metrics, nagios, mod_gearman
:slug: submit-nagios-metrics-to-graphite-with-modgearman-and-metricfactory-revisited
:status: draft

When it comes down to monitoring Nagios is still the weapon of choice for
many.  I would have abandoned it if there weren't projects like `Livestatus`_,
`Mod_Gearman`_ and `Thruk`_ which to my opinion should never be missing from
any Nagios setup.  Mod_Gearman, the framework which makes Nagios scalable, has
a feature which stores the performance data produced by the Nagios plugins
into a `Gearman`_ queue.  Graphing that performance data with `Graphite`_ is a
straightforward job with `Metricfactory`_.

Performance data
~~~~~~~~~~~~~~~~

Mod_Gearman is a Nagios addon which spreads the Nagios plugin execution over a
farm of worker nodes.  This allows you to build a scalable Nagios setup quite
effectively.  The workers execute the Nagios plugins and submit the produced
results back into the Gearman master server.  A Nagios broker module then
consumes the submitted check results from the Gearman master and submits the
check results into Nagios for further processing.  The broker module can
optionally submit the `performance data`_ back into a dedicated Gearman queue
ready to be consumed by an external process which in our case is going to be
Metricfactory.  Metricfactory will convert the performance data into the
proper format and submit that into Graphite.

Mod_Gearman
~~~~~~~~~~~~

The Mod_Gearman project has quite extensive `documentation
available`_ but these are the relevant parameters:

::

    perfdata=yes

Setting the value to *yes* makes the broker module write the
performance data to the *perfdata* queue.

::

    perfdata_mode=1

Setting the value to *1* makes sure that performance data doesn't pile up
endlessly in the queue when Metricfactory isn't consuming.  It's basically a
precaution which prevents the queue to fill up to a point all available system
memory is consumed.  Setting the value to \ *2* will append all performance
data to the queue without overwriting old data.  When enabled you can execute
the *gearman_top* command and you should see the *perfdata* queue appear:

|gearman_top|

The Jobs Waiting column indicates how many performance data is currently
stored in the queue.  Ideally this should be 0 or as low as possible and never
grow otherwise that might indicate the performance data is not consumed fast
enough. Keep in mind that not all Nagios plugins produce performance data.  If
you want to be sure whether a plugin produces performance data, have a look in
Thruk (or other Nagios interface) and verify in the service or host details
whether *Performance Data* actually contains valid perfdata.

|perfdata|

Metricfactory
~~~~~~~~~~~~~

Installation
''''''''''''

You can install Metricfactory and its dependencies from Pypi using
*easy_install*:

::

    $ easy_install metricfactory

You will require some extra Wishbone modules which can not be installed as
separate Pypi packages yet. Checkout the repository from `Github`_ and install
the module manually.

::

  $ git checkout https://github.com/smetj/wishboneModules.git

Install wb_input_gearmand

::

  $ cd wishboneModules/wb_input_gearmand
  $ python setup.py install

Install wb_output_tcp

::

  $ cd wishboneModules/wb_output_tcp
  $ python setup.py install


Quick introduction
''''''''''''''''''

Metricfactory makes use of Wishbone to build an pipeline of modules through
which events travel and change.  The setup of the Metricfactory server is
described in a bootstrapfile.  A bootstrap file contains which modules to
initialize and which path data has to follow througout these modules.

The idea behind a MetricFactory server is that it accepts metrics, converts
them into a common format, which on its turn can be processed and/or converted
again into another format.

We will gradually build up our solution by going through each step.


Consume perfdata
''''''''''''''''

First let's have a look how the perfdata looks
like when consuming it without modifications:

.. code-block:: identifier
  :linenos: table

  ---
  modules:
      gearmand:
          module: wishbone.input.gearman
          arguments:
              hostlist:
                  - server-001
              secret: changemechangeme
              queue: perfdata
              workers: 5

      decode:
          module: metricfactory.decoder.modgearman

      encode:
          module: wishbone.builtin.metrics.graphite
          arguments:
              prefix: nagios.
              script: false

      stdout:
          module: wishbone.builtin.output.stdout

  routingtable:

      - gearmand.outbox   -> stdout.inbox
      # - decode.outbox     -> encode.inbox
      # - encode.outbox     -> stdout.inbox
  ...

Depending on your environment you will have to adapt some of the variables in
the boostrap file. The *hostlist* variable (line 6) is a list of the
Gearmand servers from which the *perfdata*  has to be consumed.  Usually this
is a list containing just 1 server.  In some special cases you might add more
servers here but that's in our case not likely.

The secret variable (line 8) should contain the pre-shared encryption key
allowing you to decrypt the information consumed from Gearmand.  Worth to
mention there is no authentication, but without the decryption key you wont be
able to read the data coming from the Gearmand server.

The number of workers variable (line 10) determines how many workers should
consume the *perfdata* queue.  If you notice perdata isn't consumed fast
enough, you could bump this number to a higher value.  In this case keep an
eye on the the CPU usage of Metricfactory due to the decrypting. If you notice
Metricfactory can't keep up because of high cpu usage then another strategy
might be to leave this numer on 1 and start Metricfactory with the
*--instances x* parameter, where x is the number of parallel processes.

In this example we have connected the *gearmand.output* queue to the
*stdout.inbox* (line 26).  As a result, the perfdata will flow from the
gearmand module directly to the stdout module.

Start metricfactory in the foreground and verify whether the get the expected
output.

::

  $ metricfactory debug --config modgearmand2graphite.yaml
  DATATYPE::HOSTPERFDATA  TIMET::1383777750 HOSTNAME::aaaaaaaaaaaaa HOSTPERFDATA::rta=15.589ms;3000.000;5000.000;0; pl=0%;80;100;;  HOSTCHECKCOMMAND::check:host.alive!(null) HOSTSTATE::0  HOSTSTATETYPE::1
  DATATYPE::HOSTPERFDATA  TIMET::1383777750 HOSTNAME::bbbbbbbbbbbbb HOSTPERFDATA::rta=16.776ms;3000.000;5000.000;0; pl=0%;80;100;;  HOSTCHECKCOMMAND::check:host.alive!(null) HOSTSTATE::0  HOSTSTATETYPE::1
  DATATYPE::HOSTPERFDATA  TIMET::1383777750 HOSTNAME::ccccccccccccc HOSTPERFDATA::rta=16.559ms;3000.000;5000.000;0; pl=0%;80;100;;  HOSTCHECKCOMMAND::check:host.alive!(null) HOSTSTATE::0  HOSTSTATETYPE::1
  DATATYPE::HOSTPERFDATA  TIMET::1383777750 HOSTNAME::ddddddddddddd HOSTPERFDATA::rta=16.381ms;3000.000;5000.000;0; pl=0%;80;100;;  HOSTCHECKCOMMAND::check:host.alive!(null) HOSTSTATE::0  HOSTSTATETYPE::1
  ...snip...


Decode
''''''

The next step is to decode the perfdata into a common format.

.. code-block:: identifier
  :linenos: table

  ---
  modules:
      gearmand:
          module: wishbone.input.gearman
          arguments:
              hostlist:
                  - server-001
              secret: changemechangeme
              queue: perfdata
              workers: 5

      decode:
          module: metricfactory.decoder.modgearman

      encode:
          module: wishbone.builtin.metrics.graphite
          arguments:
              prefix: nagios.
              script: false

      stdout:
          module: wishbone.builtin.output.stdout

  routingtable:

      - gearmand.outbox   -> decode.inbox
      - decode.outbox     -> stdout.inbox
      # - encode.outbox     -> stdout.inbox
  ...


We have already defined the correct modules, so it's only a matter of changing
the data flow (line 26, 27).

::

  $ metricfactory debug --config modgearmand2graphite.yaml
  ('1383778474', 'nagios', 'aaaaaaaaaaaaa', 'hostcheck.rta', '0.000', 'ms', ('check:host.alive', 'hostcheck'))
  ('1383778474', 'nagios', 'bbbbbbbbbbbbb', 'hostcheck.pl', '100', '%', ('check:host.alive', 'hostcheck'))
  ...snip...








Converting Nagios format to graphite format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graphite stores the metrics in a tree-like hierarchical manner using a
dotted naming scheme. Somehow we will have to convert the Nagios metrics
into this format.  Metricfactory converts the metrics coming from an
external source into a common Metricfactory format.  From this format
it's straightforward to convert them into another format. Unfortunately,
many years of Nagios plugin development has lead to all kinds of metric
name formats.  This inconsistency is something we will have to deal
with. Consider following examples:

::

    rta=1.274ms;3000.000;5000.000;0; pl=0%;80;100;;

::

    /=1351MB;3426;3627;0;4031 /dev=0MB;3046;3225;0;3584 /dev/shm=0MB;3054;3233;0;3593 /boot=26MB;205;217;0;242 /tmp=16MB;427;452;0;503 /var=1430MB;6853;7256;0;8063 /var/tmp=16MB;427;452;0;503

::

    MemUsedPercent=7%;98;102;0;100 SwapUsedPercent=0%;80;90;0;100 MemUsed=486MB;;;0;7187 SwapUsed=0MB;;;0;204

The names of metrics in the first example are rta and pl respectively.
 In the second example the metric names are the paths of mount points
containing slashes.  The 3rd example has metric names with mixed
uppercase and lowercase.  Although the decode.gearman module does some
basic metric name sanitation, it's perfectly possible to write a
Wishbone module and plug it into your MetricFactory chain to convert the
metric names into whatever your like but covering that topic is out of
scope of this article. To get an idea how our data looks like after each
module we're going to alter the *routing table* in the bootstrap file
accordingly.  If you take look at our bootstrap file, you notice we have
an additional module initiated called *stdout* (line 48) which is not
included in our *routing table*.  The *stdout* module prints, as you
might guess, incoming events to STDOUT.  Let's go over each step to see
how our data looks like:

Data coming from wishbone.iomodule.Gearmand
'''''''''''''''''''''''''''''''''''''''''''

To print the data coming from Mod\_Gearman to STDOUT we change our
routing table to the following:

::

    "routingtable": {
        "modgearman.inbox": [ "stdout.inbox" ]
      }

Start Metricfactory in the foreground (`ascii.io
screencast <http://ascii.io/a/3120>`__):

::

    $ metricfactory debug --config modgearmand2graphite.json --loglevel debug

Example host performance data:

::

    DATATYPE::HOSTPERFDATA TIMET::1368178733   HOSTNAME::host_339  HOSTPERFDATA::rta=0.091ms;3000.000;5000.000;0; pl=0%;80;100;;   HOSTCHECKCOMMAND::check:host.alive!(null)   HOSTSTATE::0    HOSTSTATETYPE::1

Example service performance data:

::

    DATATYPE::SERVICEPERFDATA  TIMET::1368178797   HOSTNAME::localhost SERVICEDESC::Gearman Queues SERVICEPERFDATA::'check_results_waiting'=0;10;100;0 'check_results_running'=0 'check_results_worker'=1;25;50;0 'host_waiting'=0;10;100;0 'host_running'=0 'host_worker'=10;25;50;0 'hostgroup_localhost_waiting'=0;10;100;0 'hostgroup_localhost_running'=1 'hostgroup_localhost_worker'=10;25;50;0 'perfdata_waiting'=0;10;100;0 'perfdata_running'=0 'perfdata_worker'=1;25;50;0 'service_waiting'=0;10;100;0 'service_running'=0 'service_worker'=10;25;50;0 'worker_nagios-001_waiting'=0;10;100;0 'worker_nagios-001_running'=0 'worker_nagios-001_worker'=1;25;50;0   SERVICECHECKCOMMAND::check:app.gearman.master   SERVICESTATE::0 SERVICESTATETYPE::1

 

Data coming from metricfactory.decoder.ModGearman
'''''''''''''''''''''''''''''''''''''''''''''''''

So the data coming from Mod\_Gearman needs to be converted into the
common Metricfactory internal format.  For this we use a module from the
metricfactory.decoder group, in this case ModGearman.

Change the routing table to following configuration:

::

    "routingtable": {
        "modgearman.inbox": [ "decodemodgearman.inbox" ],
        "decodemodgearman.outbox": [ "stdout.inbox" ]
    }

Start Metricfactory in the foreground (`ascii.io
screencast <http://ascii.io/a/3121>`__):

::

    $ metricfactory debug --config modgearmand2graphite.json --loglevel debug

Example host perfdata:

::

    {'name': 'rta', 'tags': ['check:host_alive!(null)', 'hostcheck'], 'value': '0.155', 'source': 'host_409', 'time': '1368179085', 'units': 'ms', 'type': 'nagios'}

Example service perfdata:

::

    {'name': 'perfdata_waiting', 'tags': ['check:app_gearman_master', 'gearman_queues'], 'value': '0', 'source': 'localhost', 'time': '1368179129', 'units': '', 'type': 'nagios'}

The ModGearman decoder module filters out some characters from different
parts

Data coming from metricfactory.encoder.Graphite
'''''''''''''''''''''''''''''''''''''''''''''''

Now we have to convert the metrics from the internal Metricfactory
format into a the Graphite format.  The *encodegraphite* module has a
parameter \ *prefix* (line 30) which allows you to define a prefix for
the name of each metric to store in Graphite.  With this configuration,
each metric will start with "*nagios.*\ ".

Change the routing table to following configuration:

::

    "routingtable": {
        "modgearman.inbox": [ "decodemodgearman.inbox" ],
        "decodemodgearman.outbox": [ "encodegraphite.inbox" ],
        "encodegraphite.outbox": [ "stdout.inbox" ]
      }

Start Metricfactory in the foreground (`ascii.io
screencast <http://ascii.io/a/3122>`__):

::

    $ metricfactory debug --config modgearmand2graphite.json --loglevel debug

Example:

::

    nagios.host_260.hostcheck.pl 0 1368179289
    nagios.host_26.hostcheck.rta 0.133 1368179289
    nagios.host_26.hostcheck.pl 0 1368179289
    nagios.host_256.hostcheck.rta 0.123 1368179289
    nagios.localhost.gearman_queues.service_running 0 1368179329
    nagios.localhost.gearman_queues.service_worker 9 1368179329
    nagios.localhost.gearman_queues.worker_nagios-001_waiting 0 1368179329
    nagios.localhost.gearman_queues.worker_nagios-001_running 0 1368179329
    nagios.localhost.gearman_queues.worker_nagios-001_worker 1 136817932

As you can see the Graphite encoder module had to make some assumptions.
 In case the metric type is Nagios (the internal format contains this
information) then the hostchecks always have the word \ *hostcheck* in
the metric name as you can see in the above example.  When the data is a
Nagios servicecheck, then the service description is included in the
metric name.

Graphite
~~~~~~~~

Typically Nagios schedules checks every 5 minutes.  This doesn't really
result in high resolution metrics and is often used as a point of
critique.  Keep this in mind when you define a Graphite retention
policy.  In the example configuration we use \ *nagios* as a prefix
(line 30), so you could use a Whisper retention policy similar to:

::

    [nagios]
    priority = 100
    pattern = ^nagios\.
    retentions = 300:2016

Make sure the Nagios execution interval corresponds properly to
the \ *retentions* parameter to prevent gaps.

Conclusion
~~~~~~~~~~

We have covered how to setup Metricfactory to consume metric data from
ModGearman and submit that to Graphite.  We covered in detail how data
changes when traveling through the different modules to get a better
understanding of the whole process.

.. _Livestatus: http://mathias-kettner.de/checkmk_livestatus.html
.. _Mod_Gearman: http://labs.consol.de/lang/en/nagios/mod-gearman/
.. _Thruk: http://www.thruk.org/
.. _Gearman: http://gearman.org/
.. _Graphite: http://graphite.wikidot.com/
.. _Metricfactory: https://github.com/smetj/metricfactory
.. _performance data: http://nagios.sourceforge.net/docs/3_0/perfdata.html
.. _documentation available: http://labs.consol.de/lang/en/nagios/mod-gearman/
.. _Github: https://github.com/smetj/metricfactory
.. _ascii.io screencast: http://ascii.io/a/3101
.. _here: https://github.com/smetj/experiments/tree/master/metricfactory/modgearman2graphite

.. |gearman_top| image:: ../pics/submit-nagios-metrics-to-graphite-with-modgearman-and-metricfactory/gearman_top.png
   :target: ../pics/submit-nagios-metrics-to-graphite-with-modgearman-and-metricfactory/gearman_top.png

.. |perfdata| image:: ../pics/submit-nagios-metrics-to-graphite-with-modgearman-and-metricfactory/perfdata.png
   :target: ../pics/submit-nagios-metrics-to-graphite-with-modgearman-and-metricfactory/perfdata.png
