Archiving Twitter likes
#######################
:date: 2016-08-21 15:42
:author: smetj
:category: monitoring
:tags: wishbone, twitter, archive, likes
:slug: archiving_twitter_likes

__start_summary__

I use Twitter to keep track of the latest tech information by following a
tailored list of hash tags and people.  When interesting information is
shared, I like to have the possibility to archive the content for later
retrieval. *Liking* a tweet is the closest thing Twitter offers to bookmark
tweets. However, after some time you end with up with a long list of *likes* which
quickly outgrows a usable, searchable archive.

Therefor, to have a solution which suits my needs, I created a Wishbone server
to collect and archive my Twitter *likes* into an simple *"grep-able"* text
file.

__end_summary__

----

The plan
--------

The plan is to have a way to monitor my Twitter events, filter out the *like*
events, process and archive them to disk into a simple text format using
following conditions:

- For each URL in the 'liked' tweet a new entry must be made into a text file.
  Each entry should be suffixed by a comma separated list consisting out of the
  author, significant words and the hash tags.

  For example:

  ::

      - https://github.com/lenazun/working-remotely/blob/master/ideas.md (elight, working, remotely, terrific, document)



- A 'liked' tweet without URLs must be archived verbatim, prefixed with date and author.

  For example:

  ::

      - Sun Mar 11 04:41:24 +0000 2007 netik:  There is no Internet of Things. There are only many unpatched, vulnerable small computers on the Internet.


Wishbone
--------

Installation
++++++++++++

`pip` is used to install Wishbone including the necessary modules for this setup: [ref]wishbone.flow.jq requires some dependencies https://github.com/smetj/wishbone-flow-jq/blob/development/DEPENDENCIES.txt [/ref]

Although not required, I cannot recommend enough to install Wishbone into a
virtual env so you do not "pollute" your system Python installation.

.. code-block:: bash

    $ pip install wishbone-input-twitter wishbone-flow-jq wishbone-function-twitterbookmark wishbone-output-file


Bootstrap file
++++++++++++++

Starting the server


.. code-block:: bash

    $ wishbone start --config bootstrap.yaml


The bootstrap file:

[gist:id=cf30493f90ab10889d408391d7759a72,file=bootstrap.yaml]



Explaining the module instances
+++++++++++++++++++++++++++++++

input
'''''

The Twitter **input** module (*line 7)* needs the necessary authentication
information you have to acquire by creating the OAuth access tokens on
https://apps.twitter.com/.

----

filter_favs
'''''''''''

The **filter_favs** module (*line 17*) is an instance of wishbone.flow.jq and
is used to filter out the created *favorite* events.  It uses `jq`_ for
pattern matching the data structure the Twitter API returns.  The defined
condition (*line 23*) filters out the events of type "*favorite*" which have
been created by user "*smetj*".

**Obviously you will have to alter the query to match your Twitter name.**

----

bookmark
''''''''

The **bookmark** instance of `wishbone.flow.twitterbookmark`_ is where the
information I (personally) find most interesting `is extracted`_ from the
Twitter event.  Arguably this processing is perhaps not what you personally
want.  Writing your own Wishbone processing module is `quite easy`_ if you
want to do custom processing.

----

split_type, construct_bookmark, construct_text
'''''''''''''''''''''''''''''''''''''''''''''''

The *split_type* module instance splits the stream into *bookmark* and *text*
types and routes the event to the *construct_bookmark* or *construct_text*
respectively to construct the correct format (*line 50* and *line 58*) and set
the filename to write the desired output to (*line 51* and *line 59*).

----

funnel, output
''''''''''''''

The events coming out of *construct_bookmark* and *construct_text* are then
both send to the *output* module over the *funnel* module.  The *output*
module writes the value of *@tmp.result* into the filename defined in
*@tmp.filename* by the *construct_bookmark* and *construct_text* modules.

Final words
-----------

Using this setup we have seen how to bootstrap a server which collects your
Twitter likes and stores them into an easily *"grep-able"* file for later
reference.

If required, it should be really easy to modify this setup into something that
suits your specific needs.

If this is useful to you or if you have any questions about the setup, don't
hesitate to drop me a line or add a comment.


Footnotes
---------

.. _jq: https://stedolan.github.io/jq/
.. _wishbone.flow.twitterbookmark: https://github.com/smetj/wishbone-function-twitterbookmark
.. _is extracted: https://github.com/smetj/wishbone-function-twitterbookmark/blob/master/wishbone_function_twitterbookmark/twitterbookmark.py#L94
.. _quite easy: http://wishbone.readthedocs.io/en/master/examples/writing_a_module/index.html
.. _Wishbone: http://wishbone.readthedocs.org/en/latest
.. _check_http: https://www.monitoring-plugins.org/doc/man/check_http.html
.. _Pagerduty: http://www.pagerduty.com
.. _wishbone.flow.fresh: http://wishbone.readthedocs.org/en/latest/modules/builtin%20modules.html#wishbone-flow-fresh
.. _wishbone.input.httpserver: https://pypi.python.org/pypi?name=wishbone_input_httpserver&:action=display

