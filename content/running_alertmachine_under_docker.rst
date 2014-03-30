Running Alertmachine under Docker
#################################
:date: 2014-03-30 21:00
:author: smetj
:category: #monitoringlove
:tags: monitoringlove, nagios, naemon, alertmachine, docker
:slug: running_alertmachine_under_docker

xxstart_summaryxx

In a `previous article`_ I wrote about managing Naemon and Nagios alerts with
**Alertmachine**.  In this article I will cover how you can run a fully
operational *Alertmachine* container in a matter of minutes using Docker.

xxend_summaryxx

Docker
------

`Docker`_ is an open source project to pack, ship and run any application as a
lightweight container.  I have made a Docker image which contains an
Alertmachine instance including all its dependencies so it's easy to get it up
and running in no time.  To execute the steps explained in this article you
are supposed to have a running Docker instance.

Adding docker image
~~~~~~~~~~~~~~~~~~~

Before you can start to use the container you obviously have to add it to the
list of available docker images.

Adding the alertmachine image to your docker environment is done by executing
following command:

::

    $ [smetj@indigo ~]$ docker pull --tag alertmachine smetj/wishbone
    Pulling repository smetj/wishbone
    9bb81f6baa3a: Download complete
    539c0211cd76: Download complete
    7edf4f9e2b98: Download complete
    4bec87fafa27: Download complete
    2ab67fc835bf: Download complete
    [smetj@indigo ~]$


You should now be able to see the *alertmachine* image:

::

    [smetj@indigo ~]$ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    smetj/wishbone      alertmachine        9bb81f6baa3a        5 hours ago         756.2 MB
    centos              buildbox            dcee5313e217        8 days ago          1.073 GB
    centos              base                4bec87fafa27        8 days ago          662.8 MB
    centos              6.4                 539c0211cd76        12 months ago       300.6 MB
    [smetj@indigo ~]$


Running the Alertmachine container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run *Alertmachine* you need to have 3 pieces of configuration:

- The Wishbone bootstrap file
- The alert rules.
- The email templates.

I have made a repository available which you can use as a start and which we
will use as an example to complete the next steps in this article.

::

    $ git clone https://github.com/smetj/alertmachine.git


To run the alertmachine container issue following command:

::

    $ docker run -t -p 19283:19283/udp -v /home/smetj/data/projects/github/alertmachine/alertmachine:/share/alertmachine smetj/wishbone:alertmachine /usr/bin/wishbone debug --config /share/alertmachine/bootstrap/alertmachine.yaml


Now lets run over the most interesting options:

The **-p option** maps the container's port 19283/UDP to the
same port of the host.  The UDP listener is one way of receiving alert events
and is defined in the bootstrap file at `line 7`_.

The **-v option** *exposes* directory
/home/smetj/data/projects/github/alertmachine/alertmachine to the container
and "mounts" it do the **/share/alertmachine** mountpoint.  In our example,
the directory is the *alertmachine* Git repository we have clonded in a
previous step.  The `Wishbone`_ instance reads all configuration from this
location.  The advantage is this way we can keep the container more generic.
The alternative is to add the configuration inside the container so absolutely
no external dependencies exist.

**smetj/wishbone:alertmachine** defines the image we want to use.

The command we execute inside the container is:

::

    $ /usr/bin/wishbone debug --config /share/alertmachine/bootstrap/alertmachine.yaml


The yaml config file is expected to be found in the host's mounted volume as
defined by the -v switch.

We use the **debug** command to start Wishbone since that blocks the container
from exiting.

Testing Alertmachine
--------------------

We test our setup by running the container as defined in the previous step.

::

    ... snip for brevity ...
    2014-03-30T17:10:46 pid-1 informational validate: Initiated
    2014-03-30T17:10:46 pid-1 informational validate: Created module queue named inbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational validate: Created module queue named outbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational validate: Started
    2014-03-30T17:10:46 pid-1 informational validate: Function <bound method JSON.consume of <wb_function_json.wb_function_json.JSON instance at 0x1d7df38>> started to consume queue <wishbone.tools.wishbonequeue.WishboneQueue instance at 0x1d853b0>.
    2014-03-30T17:10:46 pid-1 informational match_engine: Initiated
    2014-03-30T17:10:46 pid-1 informational match_engine: Created module queue named inbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational match_engine: Created module queue named outbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational match_engine: Created module queue named email with max_size 0.
    2014-03-30T17:10:46 pid-1 informational match_engine: Started
    2014-03-30T17:10:46 pid-1 informational match_engine: Function <bound method SequentialMatch.consume of <pyseps.sequentialmatch.SequentialMatch instance at 0x1d9f4d0>> started to consume queue <wishbone.tools.wishbonequeue.WishboneQueue instance at 0x1d9f7e8>.
    2014-03-30T17:10:46 pid-1 informational email: Initiated
    2014-03-30T17:10:46 pid-1 informational email: Created module queue named inbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational email: Created module queue named outbox with max_size 0.
    2014-03-30T17:10:46 pid-1 informational email: Initialiazed.
    2014-03-30T17:10:46 pid-1 informational email: Started
    2014-03-30T17:10:46 pid-1 informational email: Function <bound method Email.consume of <wb_output_email.wb_email.Email instance at 0x1dff488>> started to consume queue <wishbone.tools.wishbonequeue.WishboneQueue instance at 0x1e0a710>.
    2014-03-30T17:10:46 pid-1 informational input_gearman: Gearmand worker instance started
    2014-03-30T17:10:46 pid-1 warning input_gearman: Connection to gearmand failed. Reason: Found no valid connections in list: [<GearmanConnection localhost:4730 connected=False>]. Retry in 1 second.
    2014-03-30T17:10:46 pid-1 informational match_engine: Monitoring directory /share/alertmachine/rules/ for changes
    2014-03-30T17:10:46 pid-1 informational match_engine: New set of rules loaded from disk


Have a look at the running Docker processes:

::

    $ docker ps
    CONTAINER ID        IMAGE                         COMMAND                CREATED             STATUS              PORTS                         NAMES
    6ea1bd4bf097        smetj/wishbone:alertmachine   /usr/bin/wishbone de   2 seconds ago       Up 2 seconds        0.0.0.0:19283->19283/udp      distracted_wozniak


Now send a `test event`_ into the container's UDP socket:

::

    $ cat sample_json_alert_event/sample.json |nc -u localhost 19283


When we return to our running Alertmachine docker terminal we should see something similar to this:

::

    {'header': {'match_engine': {'to': ['noc@your_company.local'], 'from': 'monitoring@your_company.local', 'template': 'host_email_alert', 'rule': '000-host-alert', 'subject': u'Alert - Host  some_host_001.local is  DOWN.'}}, 'data': u'Host notification.\n\nHostname                        : some_host_001.local\nIP                              : 127.0.0.1\nNotification Type               : DOWN\nTime                            : Fri Mar 21 15:30:28 CET 2014\nHost State                      : DOWN\n\nAdditional Info :\n\n        PING ok - Packet loss = 0%, RTA = 0.80 ms.'}


If you actually want and alert send out by mail instead of sending it to SDOUT you should alter the bootstrap file's `routing table`_ and connect **template.outbox** to **email.inbox**.

Final words
-----------

Docker offers an interesting approach to share and deploy Wishbone instances.
Using different bootstrap files, multiple instances could easily share the
same *rules* and *templates* directory, consume alert events from
*mod_gearman* and run in parallel.



.. _previous article: http://smetj.net/an-aleternative-way-of-handling-nagios-and-naemon-alerts.html
.. _docker: https://www.docker.io/
.. _Docker repository: https://index.docker.io/u/smetj/wishbone/
.. _line 7: https://github.com/smetj/alertmachine/blob/master/alertmachine/bootstrap/alertmachine.yaml#L7
.. _Wishbone: https://wishbone.readthedocs.org/en/latest/
.. _bootstrap file: https://github.com/smetj/alertmachine/blob/master/alertmachine/bootstrap/alertmachine.yaml#L28
.. _test event: https://github.com/smetj/alertmachine/blob/master/alertmachine/sample_json_alert_event/sample.json
.. _routing table: https://github.com/smetj/alertmachine/blob/master/alertmachine/bootstrap/alertmachine.yaml#L55