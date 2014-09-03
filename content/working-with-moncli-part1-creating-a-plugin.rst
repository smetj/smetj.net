Working with Moncli part1: Creating a plugin
############################################
:date: 2012-03-06 23:25
:author: smetj
:category: #monitoringlove
:tags: moncli
:slug: working-with-moncli-part1-creating-a-plugin

Producing data
~~~~~~~~~~~~~~

In the previous 2 posts we had an `introduction about Moncli`_ and we
have seen how to `consume Moncli data (reports) from the Message
broker with Krolyk`_ and process them.  Now its time to let Moncli
generate some data we can work with.  In the next couple of articles we
will go through the process of building a new plugin and use it to
generate metrics and perform different kind of evaluations.

Creating a simple plugin
~~~~~~~~~~~~~~~~~~~~~~~~

One of the goals for Moncli was to create a framework which allows
people to easily create their own plugins.  Although Moncli already
comes with a `set of plugins`_ which provide basic system metrics they
will not cover all your needs, so we'll create one as an example.

Let's say we want to measure and evaluate the disk space one or more
directories consume.  For this I create a small Bash/Perl oneliner which
looks like this:

::

    #!/bin/bash
    du -s -b $1\|perl -n -e '/(\\d\*)\\s\*(.\*)/ && print "$2:$1\\n"'

This script accepts 1 parameter which is the directory of which we want
to process the content.

::

    jelle@indigo:~$ ./dir_size.sh '/tmp/test/*'
    /tmp/test/one:155656192
    /tmp/test/three:4096
    /tmp/test/two:583471104
    jelle@indigo:~$

Now we have to make sure Moncli can execute this new plugin.  The name
of the plugin is dir\_size, so first we will make a new directory in the
`Moncli's repository directory`_ which contains all plugins.  The name
of the directory is the name of our script:

::

    jelle@indigo:~$ mkdir /opt/moncli/lib/repository/dir_size

Then we rename our script to the value of its md5sum and move it to the
directory we just created:

::

    jelle@indigo:~$ md5sum dir_size.sh
    a1161fc0d2dfcd6b4e9f52651e88a1d0 dir_size.sh
    jelle@indigo:~$ mv dir_size.sh /opt/moncli/lib/repository/dir_size/a1161fc0d2dfcd6b4e9f52651e88a1d0
    jelle@indigo:~$

Security
~~~~~~~~

The reason why we store the script as its md5sum is for both security as
practical reasons.  Moncli knows which script to execute because it has
the name of the directory.  The request submitted to Moncli contains
besides the name of the plugin also the md5sum of the version to
execute.  If somebody changes the content of the script, then Moncli
will not execute it, because before executing the script Moncli looks
whether the filename of the script matches its hash.  Somebody could add
a new version of the script inside the directory with the correct hash,
but then you must define that hash in your request.  In other words, you
can have multiple versions of the plugin inside the directory.

Our script is now ready to be used.

In part2 we will cover how to generate a request so we can test and use
our newly created plugin.

.. _introduction about Moncli: http://smetj.net/2012/02/09/moncli-an-introduction/
.. _consume Moncli data (reports) from the Message broker with Krolyk: http://smetj.net/2012/02/11/consuming-moncli-data-from-rabbitmq-using-krolyk/
.. _set of plugins: https://github.com/smetj/moncli/tree/master/lib/repository
.. _Moncli's repository directory: http://wiki.smetj.net/wiki/Moncli_documentation#local_repo
