New Year Python Meme 2012
#########################
:date: 2012-12-31 14:27
:author: smetj
:category: misc
:slug: new-year-python-meme-2012

Following `Tarek Ziadé's idea for a 2012 New Year Python Meme`_ here's
mine

xxend_summaryxx

What is the coolest Python application, framework or library you have discovered in 2012?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

That must be `Gevent`_.  It's possible I have been dabbling around with
it before 2012, but this year I really got into Gevent.  I really like
greenthreads and how Gevent deals with them.  When I discovered that, I
just had the urge to rewrite everything again with Gevent and
greenthreads.  Gevent really gave a boost to my Python productivity.
 Thank you `Denis Bilenko`_!

What new programming technique did you learn in 2012?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At a certain point in time we all want to have some sort of
"concurrency" between the different moving parts of the application
we're writing.  Processes, threads, async network  IO all come with
their own complexities...  For me it always boiled down to the fact I
loose oversight of the application pretty quickly once it starts to
expand.  Especially when an application is written with many callbacks.
 I don't like callbacks.  It puts a knot in my brain (and productivity)
whenever I'm working with them.  **`I personally prefer clarity over
efficiency`_** (within reason of course).  Keeping this in mind, when
going through the RabbitMQ tutorials and documentation ecosystem I came
across the concepts of `message passing`_ and the `actor model`_, this
opened for me a new way of thinking and approach to create solutions to
the problems I'm confronted with.  It allows me to visualize and
identify (both mentally as in a diagram) the different components of a
program and the interaction between them and above all avoid the
callback jungle.

What is the name of the open source project you contributed the most in 2012? What did you do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I must admit that I have been pretty much occupied with my own projects
so I haven't really contributed to any projects other than `my own`_.
 Most of my time went into creating the `WishBone`_ library.  A library
which allows one to create coroutine based event pipeline solutions.

What was the Python blog or website you read the most in 2012?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most Python information came through via Twitter.  I have recently
discovered `Python Weekly`_ and `Pycoder's weekly`_ which meanwhile have
proven to be a great source of Python info.

What are the three top things you want to learn in 2013?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

More than 3 things I would say, but I'll start with this list:

#. Explore and learn the new stuff Python 3.3 brings.
#. ZeroMQ and its Python bindings.
#. More on metric analysis...

What are the top software, app or lib you wish someone would write in 2013?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A killer bookmark manager in my browser to manage my delicious
bookmarks.

.. _Tarek Ziadé's idea for a 2012 New Year Python Meme: http://blog.ziade.org/2012/12/23/new-years-python-meme-2012/
.. _Gevent: http://www.gevent.org/
.. _Denis Bilenko: http://denisbilenko.com/
.. _I personally prefer clarity over efficiency: http://www.faqs.org/docs/artu/ch01s06.html
.. _message passing: http://en.wikipedia.org/wiki/Message_passing
.. _actor model: http://en.wikipedia.org/wiki/Actor_model#Fundamental_concepts
.. _my own: https://github.com/smetj
.. _WishBone: https://github.com/smetj/wishbone
.. _Python Weekly: http://www.pythonweekly.com/
.. _Pycoder's weekly: http://pycoders.com/
