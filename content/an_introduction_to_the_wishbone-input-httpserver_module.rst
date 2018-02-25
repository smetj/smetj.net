An introduction to the wishbone-input-httpserver module
#######################################################
:date: 2018-02-25 14:40
:author: smetj
:category: wishbone
:tags: wishbone, http, webhooks, payload, events
:slug: an_introduction_to_the_wishbone-input-httpserver_module

.. role:: text(code)
   :language: text

__start_summary__

In this article we will explore the current version of :text:`wishbone-input-httpserver`
a *Wishbone* input module to receive events over http(s).

__end_summary__


----


Introduction
------------

:text:`Wishbone-input-httpserver` is a `wishbone`_ `input module`_ to receive
events over the http protocol.  A typical use-case is to accept and process
webhook payloads. Once the payload is received, it is turned into an event
which can be further processed and acted upon as defined by the *Wishbone*
bootstrap file.

The source code can be found on Github: https://github.com/wishbone-modules/wishbone-input-httpserver


Installation & setup
--------------------

Both *Wishbone* and *wishbone-input-httpserver* can be installed in different
ways. The Wishbone `installation documentation`_ describes the most common
scenarios.

In this article we will use the Docker image
:text:`smetj/wishbone-input-httpserver:development` which is build by
`travis-ci`_ each time code is committed to the project or a new release is
done.

This container image includes the latest *Wishbone* and *wishbone-input-
httpserver* and is used as a reference installation.


Validate module availability
++++++++++++++++++++++++++++

You can validate whether the :text:`wishbone-input-httpserver` module is available by issuing following command:

.. code-block:: sh

    $ docker run -t -i smetj/wishbone-input-httpserver:development list

If *Wishbone* can find the *wishbone-input-httpserver* module it will be
listed as :text:`wishbone_contrib.module.input.httpserver` since it is not a
builtin module but an external (contributed) one instead.


Bootstrap file
++++++++++++++

The `bootstrap file`_ defines the Wishbone server.  It defines which modules
to initialize using which parameters and which module queues to connect in
order to define the event flow.

We will use the following bootstrap file as starting point for this article:

[gist:id=8cc3ef80628d591ba1d907ddd125f8c8,file=bootstrap_1.yaml]



To bootstrap the Wishbone server we mount the bootstrap file to the container:

.. code-block:: text

    $ docker run -t -i \
        --volume $(pwd)/bootstrap.yaml:/bootstrap.yaml \
        -p 19283:19283 \
        smetj/wishbone-input-httpserver:development start --config /bootstrap.yaml



If all went well you should have a running Wishbone server greeting you with
following message:

.. code-block:: text

    Instance started in foreground with pid 1
    2018-02-22T12:03:29.7677+00:00 wishbone[1] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests


Documentation
+++++++++++++

At any time you can read a module's documentation using following command:

.. code-block:: sh

    $ docker run -t -i smetj/wishbone-input-httpserver:development show --docs wishbone_contrib.module.input.httpserver


Features
--------


Paths vs queues
+++++++++++++++

Wishbone modules are connected to each other with queues.

The example bootstrap file connects the :text:`input` queue of 2
:text:`wishbone.module.output.stdout` module instances (*red and green*) to
the :text:`red` and :text:`green` queue of module instance :text:`input`.

This means that events submitted to :text:`http://localhost:19283/green` will
end up with module instance :text:`green` and events submitted to
:text:`http://localhost:19283/red` will end up with module instance
:text:`green`.

The URL path is mapped to a queue name, therefor the path should always match a
queue name otherwise you will get a 404:

.. code-block:: text

    $ curl http://localhost:19283/red/three/four
    404 Not Found. Endpoint 'red/three/four' does not exist

    $ curl http://localhost:19283/blue
    404 Not Found. Endpoint 'blue' does not exist


Submitting data
+++++++++++++++

A client can submit data using a PUT or POST on the desired resource:

.. code-block:: text

    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -d @- http://localhost:19283/green
    200 OK. 28cfaced-598c-4b33-bd19-ba1efa0c613d

On the server side we can see the payload embedded in an event and printed to STDOUT (module instance :text:`green`):

.. code-block:: text

    Instance started in foreground with pid 1
    2018-02-23T15:54:52.8308+00:00 wishbone[1] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests
    {'cloned': False, 'bulk': False, 'data': {'one': 1, 'two': 2, 'three': 3}, 'errors': {}, 'tags': [], 'timestamp': 1519401293.4195442, 'tmp': {'input': {'headers': {'content-type': 'application/x-www-form-urlencoded', 'content-length': '32', 'host': 'localhost:19283', 'user-agent': 'curl/7.53.1', 'accept': '*/*'}, 'env': {'gateway_interface': 'CGI/1.1', 'server_software': 'gevent/1.2 Python/3.6', 'script_name': '', 'wsgi.url_scheme': 'http', 'server_name': '42ac480639ed', 'server_port': '19283', 'request_method': 'PUT', 'path_info': '/green', 'query_string': '', 'content_type': 'application/x-www-form-urlencoded', 'content_length': '32', 'server_protocol': 'HTTP/1.1', 'remote_addr': '172.17.0.1', 'remote_port': '38236', 'http_host': 'localhost:19283', 'http_user_agent': 'curl/7.53.1', 'http_accept': '*/*'}, 'params': {}}, 'green': {}}, 'ttl': 253, 'uuid_previous': [], 'uuid': '28cfaced-598c-4b33-bd19-ba1efa0c613d'}
    2018-02-23T15:54:53.4217+00:00 wishbone[1] informational input: 172.17.0.1 - - [2018-02-23 15:54:53] "PUT /green HTTP/1.1" 200 167 0.000790


The bootstrap file has defined a :text:`wishbone.protocol.decode.json`
instances called :text:`json` which is applied to the :text:`input` module
instance.

As you can see, the UUID returned to the client is also available in the event itself.

If we were to submit invalid JSON we would get following error:

.. code-block:: text

    $ echo 'abc'|curl -XPUT -d @- http://localhost:19283/green
    406 Not Acceptable. There was an error processing your request. Reason: ProtocolDecodeError Expecting value: line 1 column 1 (char 0)



URL query string for extra context
++++++++++++++++++++++++++++++++++

Sometimes you could use the possibility to add additional context to a payload
without having the opportunity to modify the payload itself.  Think of for
example the many webhook functionality offered by service such as Github,
Pagerduty, Docker registry, ...

The :text:`wishbone-input-httpserver` module accepts an URL query string for
each endpoint. This doesn't really influence the request itself but instead it
adds the query string's key/values to the Wishbone event's metadata.

An example illustrates the usage:

A client request:

.. code-block:: text

    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -d @- 'http://localhost:19283/green?&location=eu&country=be&city=brussels'
    200 OK. 6838ab83-2b32-4ac2-b32a-e3bc3d0b92ff

On the server side:

.. code-block:: text
    Instance started in foreground with pid 1
    2018-02-24T15:10:59.5264+00:00 wishbone[1] informational input: 172.17.0.1 - - [2018-02-24 15:10:59] "PUT /green? HTTP/1.1" 200 167 0.000693

    {'cloned': False, 'bulk': False, 'data': {'one': 1, 'two': 2, 'three': 3}, 'errors': {}, 'tags': [], 'timestamp': 1519485068.251564, 'tmp': {'input': {'headers': {'content-type': 'application/x-www-form-urlencoded', 'content-length': '32', 'host': 'localhost:19283', 'user-agent': 'curl/7.53.1', 'accept': '*/*'}, 'env': {'gateway_interface': 'CGI/1.1', 'server_software': 'gevent/1.2 Python/3.6', 'script_name': '', 'wsgi.url_scheme': 'http', 'server_name': 'd47dcd83a746', 'server_port': '19283', 'request_method': 'PUT', 'path_info': '/green', 'query_string': '&location=eu&country=be&city=brussels', 'content_type': 'application/x-www-form-urlencoded', 'content_length': '32', 'server_protocol': 'HTTP/1.1', 'remote_addr': '172.17.0.1', 'remote_port': '56856', 'http_host': 'localhost:19283', 'http_user_agent': 'curl/7.53.1', 'http_accept': '*/*'}, 'params': {'location': 'eu', 'country': 'be', 'city': 'brussels'}}, 'green': {}}, 'ttl': 253, 'uuid_previous': [], 'uuid': '6838ab83-2b32-4ac2-b32a-e3bc3d0b92ff'}


As you can see the :text:`tmp.input.params` contains the query parameters as
key/values which can be useful for further processing. This way we can give
the client the possibility add additional contextual data to the event without
having to modify the actual payload.


Multiple instances
++++++++++++++++++

Using the module parameter :text:`so_reuseport` you can, if desired, run
multiple Wishbone processes and have each :text:`wishbone-input-httpserver`
instance bind to the same port.  The result of this is that each incoming
request is handled in a round robin fashion by the server instances bound to
that port.

For this we set following option in the bootstrap file:

.. code-block:: yaml

    modules:
      input:
        module: wishbone_contrib.module.input.httpserver
        protocol: json
        arguments:
            so_reuseport: true

We start the Wishbone server using following option :text:`--instances 2`:

.. code-block:: text

    $ docker run -t -i \
    --volume $(pwd)/bootstrap.yaml:/bootstrap.yaml \
    -p 19283:19283 \
    smetj/wishbone-input-httpserver:development start --config /bootstrap.yaml --instances 2

    Instances started in foreground with pid 9, 10
    2018-02-24T15:59:31.7313+00:00 wishbone[10] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests
    2018-02-24T15:59:31.7321+00:00 wishbone[9] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests


We can see incoming requests are spread round robin over both instances by
looking at the PID in the logs:

.. code-block:: text

    2018-02-24T15:59:31.7313+00:00 wishbone[10] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests
    2018-02-24T15:59:31.7321+00:00 wishbone[9] informational input: Webserver bound to 0.0.0.0:19283. Listening for incoming requests
    {'cloned': False, 'bulk': False, 'data': {'one': 1, 'two': 2, 'three': 3}, 'errors': {}, 'tags': [], 'timestamp': 1519488117.1167986, 'tmp': {'input': {'headers': {'content-type': 'application/x-www-form-urlencoded', 'content-length': '32', 'host': 'localhost:19283', 'user-agent': 'curl/7.53.1', 'accept': '*/*'}, 'env': {'gateway_interface': 'CGI/1.1', 'server_software': 'gevent/1.2 Python/3.6', 'script_name': '', 'wsgi.url_scheme': 'http', 'server_name': 'd1c2cff05487', 'server_port': '19283', 'request_method': 'PUT', 'path_info': '/green', 'query_string': '&location=eu&country=be&city=brussels', 'content_type': 'application/x-www-form-urlencoded', 'content_length': '32', 'server_protocol': 'HTTP/1.1', 'remote_addr': '172.17.0.1', 'remote_port': '57332', 'http_host': 'localhost:19283', 'http_user_agent': 'curl/7.53.1', 'http_accept': '*/*'}, 'params': {'location': 'eu', 'country': 'be', 'city': 'brussels'}}, 'green': {}}, 'ttl': 253, 'uuid_previous': [], 'uuid': '561f38d2-c0a2-4fd9-a733-e85d4ad399b3'}
    2018-02-24T16:01:57.1194+00:00 wishbone[9] informational input: 172.17.0.1 - - [2018-02-24 16:01:57] "PUT /green?&location=eu&country=be&city=brussels HTTP/1.1" 200 167 0.000814
    {'cloned': False, 'bulk': False, 'data': {'one': 1, 'two': 2, 'three': 3}, 'errors': {}, 'tags': [], 'timestamp': 1519488117.6960216, 'tmp': {'input': {'headers': {'content-type': 'application/x-www-form-urlencoded', 'content-length': '32', 'host': 'localhost:19283', 'user-agent': 'curl/7.53.1', 'accept': '*/*'}, 'env': {'gateway_interface': 'CGI/1.1', 'server_software': 'gevent/1.2 Python/3.6', 'script_name': '', 'wsgi.url_scheme': 'http', 'server_name': 'd1c2cff05487', 'server_port': '19283', 'request_method': 'PUT', 'path_info': '/green', 'query_string': '&location=eu&country=be&city=brussels', 'content_type': 'application/x-www-form-urlencoded', 'content_length': '32', 'server_protocol': 'HTTP/1.1', 'remote_addr': '172.17.0.1', 'remote_port': '57336', 'http_host': 'localhost:19283', 'http_user_agent': 'curl/7.53.1', 'http_accept': '*/*'}, 'params': {'location': 'eu', 'country': 'be', 'city': 'brussels'}}, 'green': {}}, 'ttl': 253, 'uuid_previous': [], 'uuid': '926d9b41-f07e-4ab0-a607-d3166d3437f1'}
    2018-02-24T16:01:57.6988+00:00 wishbone[10] informational input: 172.17.0.1 - - [2018-02-24 16:01:57] "PUT /green?&location=eu&country=be&city=brussels HTTP/1.1" 200 167 0.000798



Responses
+++++++++

:text:`wishbone-input-httpserver` offers the possibility to set a custom
response to the client in case of a 200.

We can set custom responses per endpoint by setting the :text:`resource`
parameter in bootstrap file:

.. code-block:: yaml

    modules:
      input:
        module: wishbone_contrib.module.input.httpserver
        protocol: json
        arguments:
            resource:
                '(green|red)':
                    users: []
                    tokens: []
                    response: "200 How is the weather in {{tmp.input.params.city}}?"


The response on the client side then looks like:

.. code-block:: text

    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -d @- 'http://localhost:19283/green?&location=eu&country=be&city=brussels'
    200 How is the weather in brussels?


The :text:`resource` parameter is a *dict* of which the key is a :text:`regex`
matching the endpoint.  The value is a dict consisting out of :text:`users`,
:text:`tokens`:text:`response`.


Authentication
--------------

Per defined *resource* in the :text:`resource` parameter you can define
authentication using a token or basic authentication.

Once a user (for basic authentication) or a token is defined, the endpoints
matching the regex require authentication.

----

**Obviously, when authentication comes in play (and even without), you should run**
:text:`wishbone-input-httpserver` **with SSL certificates by setting the**
:text:`ssl_key`, :text:`ssl_cert` **and** :text:`ssl_cacerts` **module parameters.**

----

Token based authentication
++++++++++++++++++++++++++

Enabling token authentication is as simple as adding a value to the tokens
*array* of the resource in the :text:`resource` parameter:

.. code-block:: yaml

    modules:
      input:
        module: wishbone_contrib.module.input.httpserver
        protocol: json
        arguments:
            resource:
                '(green|red)':
                    users: []
                    tokens:
                        - 6cdd782b63624c5ab6a6635112557a30
                    response: "200 How is the weather in {{tmp.input.params.city}}?"

The client request:

.. code-block:: text

    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -d @- 'http://localhost:19283/green?&location=eu&country=be&city=brussels'
    403 Unauthorized. The requested resource requires authentication.
    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -H 'Authorization: token 6cdd782b63624c5ab6a6635112557a30' -d @- 'http://localhost:19283/green?&location=eu&country=be&city=brussels'
    200 How is the weather in brussels?


Basic authentication
++++++++++++++++++++

Basic authentication requires you to set 2 values.  You need to associate the
username to the resource (:text:`users` value) and you need to define the
username and hashed password in :text:`htpasswd` module parameter.

The :text:`htpasswd` parameter is a *dict* where keys are usernames and the
values are hashed passwords. The hashed passwords can be created by using the
:text:`htpasswd` command:

.. code-block:: text

    $ htpasswd -n -b bob my_secret_password
    bob:$apr1$96XNBTbu$Gpw.UY6op/TG06Uba21ck/

You can then add the user and the hashed password to the module parameters:


.. code-block:: yaml

    modules:
      input:
        module: wishbone_contrib.module.input.httpserver
        protocol: json
        arguments:
            resource:
                '(green|red)':
                    users:
                        - bob
                    tokens:
                        - 6cdd782b63624c5ab6a6635112557a30
                    response: "200 How is the weather in {{tmp.input.params.city}}?"
            htpasswd:
                bob: '$apr1$96XNBTbu$Gpw.UY6op/TG06Uba21ck/'

Client side:

.. code-block:: text

    $ echo '{"one": 1, "two": 2, "three": 3}'|curl -XPUT -d @- 'http://bob:my_secret_password@localhost:19283/green?&location=eu&country=be&city=brussels'
    200 How is the weather in brussels?



Update authentication & authorization without restart
-----------------------------------------------------

Depending on the use case, having to restart the server in order to load
updated credentials isn't very practical.

The :text:`wishbone-input-httpserver` module comes with 2 special queues
:text:`_resource` and :text:`_htpasswd` which can receive events triggering
the reload of on disk based *resource* or *htpasswd* file.

The format of the incoming event should be:

.. code-block:: json

    {"path": "/var/tmp/htpasswd", "inotify_type": "IN_CLOSE_WRITE"}


You can somehow create these type of events yourself or you can use the
builtin Wishbone module `wishbone.module.input.inotify`_ which can monitor
files for changes and generate the required events for
:text:`wishbone-input-httpserver` to reload the file.

The following bootstrap file illustrates the idea:

[gist:id=8cc3ef80628d591ba1d907ddd125f8c8,file=bootstrap_2.yaml]

When running the server you should the htpasswd file from the host.


.. code-block:: text

    $ docker run -t -i \
      --volume $(pwd)/htpasswd:/htpasswd \
      --volume $(pwd)/bootstrap_2.yaml:/bootstrap.yaml \
      -p 19283:19283 \
      smetj/wishbone-input-httpserver:development start --config /bootstrap.yaml

Updating Bob's password:

.. code-block:: text

    $ htpasswd -b ./htpasswd bob abc

The Wishbone server's :text:`wishbone-input-httpserver` instance reports the
htpasswd is read:

.. code-block:: test

    2018-02-25T12:09:48.4312+00:00 wishbone[1] informational input: Reading htpasswd file '/htpasswd'. Cached.


Where to go from here
---------------------

In this article we have reviewed the main features of the
:text:`wishbone-input-httpserver` module.

Obviously, sending incoming events to STDOUT is handy for exploring and
experimenting but otherwise it's not that useful as such.

First of all, it's really easy to `create your own wishbone module`_.  So
extending Wishbone with your own custom code isn't hard.

Besides that, there are a number of *Wishbone 3* compatible modules available
on the `wishbone modules`_ Github account and more on their way.

Any feedback, comments, suggestions, bug reports, pull requests are highly
welcome and highly appreciated.


.. _installation documentation: http://wishbone.readthedocs.io/en/master/installation/index.html
.. _wishbone: http://wishbone.readthedocs.io
.. _httpserver: https://github.com/wishbone-modules/wishbone-input-httpserver
.. _wishbone-input-httpserver: https://github.com/wishbone-modules/wishbone-input-httpserver
.. _input module: http://wishbone.readthedocs.io/en/master/components/modules/input.html
.. _travis-ci: https://travis-ci.org/wishbone-modules/wishbone-input-httpserver
.. _bootstrap file: http://wishbone.readthedocs.io/en/master/bootstrap_cli/bootstrap_file.html
.. _wishbone.module.input.inotify: http://wishbone.readthedocs.io/en/master/classes/input_modules.html#wishbone.module.wb_inotify.WBInotify
.. _create your own wishbone module: http://wishbone.readthedocs.io/en/master/examples_recipes/creating_a_module.html
.. _wishbone modules: https://github.com/wishbone-modules
