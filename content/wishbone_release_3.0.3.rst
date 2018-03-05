Wishbone release 3.0.3
######################
:date: 2018-03-05 20:00
:author: smetj
:category: development
:tags: wishbone, release
:slug: wishbone_release_3.0.3

.. role:: text(code)
   :language: text

__start_summary__

Wishbone 3.0.3 release.

__end_summary__


----

Documentation
-------------

https://wishbone.readthedocs.io


Downloads
---------

Download release directly from Github: https://github.com/smetj/wishbone/releases/tag/3.0.3

Download updated Docker container: :text:`smetj/wishbone:3.0.3`


Builds and testing
------------------

https://travis-ci.org/smetj/wishbone


Highlights
----------

- `Input modules`_ **always** require a :text:`native_event` and :text:`destination` parameter.

  :text:`native_event` defines whether the incoming events are *native wishbone events*.
  :text:`destination` defines the field in which the incoming data needs to be stored. (default is data)

- `Output modules`_ **always** require a :text:`native_event`, :text:`selection` and :text:`payload` parameter.

  :text:`native_event` defines whether the outgoing events are *native
  wishbone events*.  :text:`selection` defines the event field to submit.
  :text:`payload` defines a template to submit. :text:`native_event` takes
  precedence over :text:`payload` which takes precedence over :text:`selection`.

  Using :text:`wishbone.module.Output.getDataToSubmit()` automatically takes
  care of this logic.

- :text:`Actor.generateEvent()` is now  :text:`native_event` aware for `Input modules`_.

- :text:`Actor.generateEvent()` can now render templates and template nested in datastructures.



Errata
------

- From this release on, Docker images are `Alpine Linux`_ based.



.. _Input modules: http://wishbone.readthedocs.io/en/latest/components/modules/input.html
.. _Output modules: http://wishbone.readthedocs.io/en/latest/components/modules/output.html
.. _Alpine Linux: https://alpinelinux.org/
