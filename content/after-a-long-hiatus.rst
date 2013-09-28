After a long hiatus
###################
:date: 2012-09-30 23:46
:author: smetj
:category: monitoring
:tags: molog, monitoring
:slug: after-a-long-hiatus

Finally after finishing a whole bunch of private "projects", I'm able to
spend some more time again to the `various open source projects`_ I've
been working on until now.  I have gathered a whole bunch of new ideas,
processed good and bad feedback, experienced that some ideas just don't
work out while others are quite encouraging.

I haven't been totally unproductive though.  I have been able to spend
time writing the Python \ `Wishbone`_ library.  The Wishbone library is
a lightweight way of writing multiple gevent based parallel processes
which connect multiple modules through an internal message passing
interface into a clean workflow.

I have also created `MonFS`_ which is a Fuse filesystem plugin allowing
you to store your Nagios (or compatible) configuration into a MongoDB
and mount that database as a read-only filesystem containing Nagios
configuration files.

The projects which currently gets most attention is `MoLog`_.  The
latest development which is a complete rewrite, is currently sitting in
the *molog\_based* branch.  I've split MoLog into 3  parts:  The main
engine, a RESTful API and a CLI.  The main engine has been
rewritten using the Wishbone and it seems to work reasonably fast even
without doing any optimization and without doing any profiling to
identify existing hot spots.

It's time to roll up the sleeves and start to do some useful tinkering
and coding again.

.. _various open source projects: https://github.com/smetj
.. _Wishbone: https://github.com/smetj/wishbone
.. _MonFS: https://github.com/smetj/monfs
.. _MoLog: https://github.com/smetj/molog/tree/wishbone_based
