Wishbone release 3.1.0
######################
:date: 2018-03-17 10:00
:author: smetj
:category: technology
:slug: wishbone_release_3.1.0

.. role:: text(code)
   :language: text



Wishbone 3.1.0 release.





Documentation
-------------

https://wishbone.readthedocs.io


Downloads
---------

Download release directly from Github: https://github.com/smetj/wishbone/releases/tag/3.1.0

Download updated Docker container: :text:`smetj/wishbone:3.1.0`


Builds and testing
------------------

https://travis-ci.org/smetj/wishbone


Release notes
-------------

    Features:
        - Added wishbone.module.output.throughput
        - Some minor speed improvements prevening useless template rendering where
          string can't be a template.
        - Added debug log showing the module version
        - Fixed docstrings of protocol decode modules
        - Added wishbone.protocol.encode.binary
        - Added parallel streams support for output modules

    Changes:
        - Changed ``native_event`` parameter to ``native_events``
        - Added new feature ``parallel_streams`` for output modules


Errata
------

- All Wishbone external modules https://github.com/wishbone-modules have been
  updated for :text:`wishbone-3.1.0`.
