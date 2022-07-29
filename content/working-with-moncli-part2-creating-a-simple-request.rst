Working with Moncli part2: Creating a simple request
####################################################
:date: 2012-03-11 22:12
:author: smetj
:category: technology
:slug: working-with-moncli-part2-creating-a-simple-request
:tags:

In our `previous post`_ we have covered how to create an example plugin
which allows you to generate the size of directories as a metric. A
plugin on itself doesn't do that much at all. When a plugin is executed
it returns the values of that very moment. Executing a plugin is done
by Moncli itself and we want to have control over that as much as
possible.

moncli\_request
~~~~~~~~~~~~~~~

`A request is a JSON document`_ which is submitted to the message broker
on which the Moncli clients are listening for incoming requests.
Creating and submitting a request could be doneby hand, but that's not
practical at all. `Moncli\_request`_ is a simple request generator tool
which generates and submits a valid JSON document to Moncli to work
with. Let's generate a request for our dir\_size plugin we created in
the previous article. Moncli\_request takes a base JSON document and
completes it with the parameters you feed to it. So let run through
the required steps:

#. Install moncli\_request from git:

   ::

       $ git clone https://smetj@github.com/smetj/moncli_request.git /opt/moncli_request

#. Copy the skeleton base document over to a new default check called
   DirSize:

   ::

       $ cp /opt/moncli_request/repository/skeleton /opt/moncli_request/repository/.default/DirSize

#. Complete our newly created DirSize base document with the plugin name
   and hash:

   ::

       {
        "plugin":{
        "name":"dir_size",
        "hash":"a1161fc0d2dfcd6b4e9f52651e88a1d0",
        "timeout":60
        },
        "report":{
        "message":""
        },
        "request":{
        "cycle":60
        },
        "evaluators":{
        },
        "tags":[]
       }

   The name is the name of the plugin we created in the previous post
   and stored in Moncli's local repository. This actually corresponds
   to the directory name containing the plugin. The hash is the md5sum
   of the plugin. Parameters is a list of parameters we want to feed to
   the script.

#. Now execute moncli\_request without the --broker parameter. This
   will print the request which you can submit to Moncli through the
   message broker on STDOUT:

   ::

       $ /opt/moncli_request/moncli_request --host indigo --subject 'DirSize' --parameters [\"\'/tmp/test/*\'\"]
       {"request":{"source":"indigo","month":3,"week_of_year":10,"time":"2012-03-11T19:58:54+01:00","day_of_year":71,"uuid":"DDB2AFC8-6BA3-11E1-B62D-8DA2DAFBAEBF","day":11,"day_of_week":7,"cycle":60,"year":2012},"plugin":{"parameters":["'/tmp/test/*'"],"hash":"a1161fc0d2dfcd6b4e9f52651e88a1d0","timeout":60,"name":"dir_size"},"report":{"message":""},"destination":{"subject":"DirSize","name":"indigo"},"evaluators":{},"tags":[]}

   .. raw:: html

      <div>

   .. raw:: html

      </div>

#. After verifying the content we can 'inject' the request into the
   message broker on which Moncli is listening:

::

    $ /opt/moncli_request/moncli_request --broker sandbox --host sandbox --subject 'DirSize' --parameters [\"\'/tmp/test/*\'\"]
    A new Report Request (7373E8A2-6B6C-11E1-A438-D193DAFBAEBF) has been submitted.

Keep in mind that the --broker parameter is the address/hostname of your
broker and the --host is the hostname of the host on which Moncli is
started. Each started Moncli instance creates a queue in the broker
with its hostname as the queue name.

Report
~~~~~~

When we consume the result from the broker (`see this post`_) we get
following result:

::

    {
       "evaluators":{

       },
       "tags":[

       ],
       "destination":{
          "name":"indigo",
          "subject":"DirSize"
       },
       "request":{
          "uuid":"3FF36DE4-6BA4-11E1-8B44-B4A2DAFBAEBF",
          "year":2012,
          "day_of_year":71,
          "day_of_week":7,
          "month":3,
          "source":"indigo",
          "week_of_year":10,
          "time":"2012-03-11T20:01:38+01:00",
          "day":11,
          "cycle":60
       },
       "report":{
          "month":3,
          "year":2012,
          "timezone":"+0100",
          "message":"",
          "day":11,
          "uuid":"35672bb1-2cb8-46ea-8e23-bf5b98cbeaf4",
          "day_of_year":71,
          "day_of_week":0,
          "source":"indigo",
          "week_of_year":10,
          "time":"2012-03-11T19:02:06+0100"
       },
       "plugin":{
          "metrics":{
             "pre_epoch":1331488926.0,
             "/tmp/test/2":"24576",
             "/tmp/test/1":"24576",
             "pre_/tmp/test/1":"24576",
             "pre_/tmp/test/3":"24576",
             "pre_/tmp/test/2":"24576",
             "/tmp/test/3":"24576",
             "epoch":1331488926.0
          },
          "raw":[
             "/tmp/test/1:24576\n",
             "/tmp/test/2:24576\n",
             "/tmp/test/3:24576\n"
          ],
          "name":"dir_size",
          "verbose":[

          ]
       }
    }

Conclusion:
~~~~~~~~~~~

We have seen how to create a plugin and how to generate a request for
it. We let Moncli execute the plugin by generating and submitting a
request with moncli\_request and we have verified the incoming results.
In this request we haven't done any evaluations which is something we
will cover in the next article in this series.



.. _previous post: http://smetj.net/2012/03/06/working-with-moncli-part1-creating-a-plugin/
.. _A request is a JSON document: http://wiki.smetj.net/wiki/Moncli_documentation#Request
.. _Moncli\_request: https://github.com/smetj/moncli_request
.. _see this post: http://smetj.net/2012/02/11/consuming-moncli-data-from-rabbitmq-using-krolyk/
