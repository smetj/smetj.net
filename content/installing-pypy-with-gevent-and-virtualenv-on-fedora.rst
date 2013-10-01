Installing PyPy with Gevent and virtualenv on Fedora
####################################################
:date: 2013-06-05 01:26
:author: smetj
:category: development
:tags: python, gevent, pypy
:slug: installing-pypy-with-gevent-and-virtualenv-on-fedora

PyPy has been on my radar for a while but I have never really brought
myself to the point of actually trying it.  Recently, a notification
caught to my attention stating PyPy 2.0.2 was released and had support
to run Gevent.  Good news! I was looking at speed improvements for
my \ `Wishbone library`_ and decided to spend some effort into getting
PyPy with Gevent up and running.  The information available explaining
how to setup Gevent in PyPy is rather sparse which might be a bit time
consuming when you have to figure out the bits and pieces.  After some
tinkering I got PyPy with Gevent up and running within virtualenv on a
Fedora host.  Here are my notes, It might be useful for you to and save
some previous time:

Before you proceed make sure you have read the
"`building-from-source`_\ " instructions from the PyPy site.

Compiling
~~~~~~~~~

PyPy has some binaries available but they can only be used on Ubuntu so
we'll have to download the source and compile from scratch.

Start by `downloading the source`_ and unpack the tarball.

::

    $ tar -xvjf pypy-2.0.2-src.tar.bz2

Before starting to compile make sure we have all required libraries
installed:

::

    $ yum install openssl-devel libffi-devel ncurses-devel expat-devel bzip2-devel

Move into our unpacked directory and start the compilation.  In the
below examples we use the Python version which comes with your os to run
the compilation process.

::

    $ cd pypy-2.0.2-src/pypy/goal
    $ python ../../rpython/bin/rpython --opt=jit targetpypystandalone.py

The compilation process is fairly lengthy.  It took +- 90 minutes(!) on
my laptop for the process to finish.

Prepare the installation
~~~~~~~~~~~~~~~~~~~~~~~~

When the compilation has finished we should have a file called
*pypy-c* in the current directory.

Best is to move the complete install to the /opt/ directory and
rename the directory appropriately.

::

    $ mv pypy-2.0.2-src /opt/pypy-2.0.2

Now let's use virtualenv to create an isolated instance of PyPy, keeping
your freshly compiled one clean:

::

    $ virtualenv -p /opt/pypy-2.0.2/pypy/goal/pypy-c ~/pypy-2.0.2
    $ . ~/pypy-2.0.2/bin/activate

Gevent
~~~~~~

First make sure you have following library installed:

::

    $ yum install libev-devel

Install the `cffi`_ module:

::

    (pypy-2.0.2)$ pip install cffi

Install a `version of Gevent`_ which has been modified to run on PyPy.
 Make sure we install Gevent inside our virtualenv:

::

    $ git clone https://github.com/schmir/gevent.git
    $ cd gevent
    $ git checkout pypy-hacks
    $ . ~/pypy-2.0.2/bin/activate
    (pypy-2.0.2)$ pypy setup.py install

Now we need one last modification which implements gevent.core as cffi
module:

::

    $ git clone https://github.com/gevent-on-pypy/pypycore.git
    $ cd pypycore
    $ . ~/pypy-2.0.2/bin/activate
    (pypy-2.0.2)$ CFLAGS=-O2 pip install -e .

If setup.py complains it can not locate *ev.h* it's possible the library
search path isn't complete.  In that case locate the location of the
file and add that directory to pypycore.py (starts at line 207) using
the *include\_dirs* variable:

::

    libev = C = ffi.verify("""   // passed to the real C compiler
    #include

    void gevent_noop(struct ev_loop *_loop, void *watcher, int revents) { }
    """, libraries=["ev"], include_dirs=["/usr/include/libev"])

Test
~~~~

Before starting \ *PyPy* we have to make sure gevent used the right
gevent.core:\ *
*

::

    $ export GEVENT_LOOP=pypycore.loop

Now start PyPy and execute some gevent code:

::

    $ . ~/pypy-2.0.2/bin/activate
    (pypy-2.0.2)$ pypy
    Python 2.7.3 (5acfe049a5b0cd0de158f62553a98f5ef364fd29, Jun 01 2013, 08:37:22)
    [PyPy 2.0.2 with GCC 4.7.2 20121109 (Red Hat 4.7.2-8)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    And now for something completely different: ``PyPy 1.3 released (windows
    binaries included)''
    >>>> import gevent
    >>>> for _ in xrange(100):
    ....     gevent.spawn(gevent.sleep, 1)

Conclusion
~~~~~~~~~~

As you can see setting up PyPy with Gevent requires a bit of work.  Once setup
into a virtualenv it's really easy to use, experiment and rebuild.

*Have a lot of fun running Gevent on PyPy!*

.. _Wishbone library: https://github.com/smetj/wishbone
.. _building-from-source: http://pypy.org/download.html#building-from-source
.. _downloading the source: http://pypy.org/download.html
.. _cffi: https://pypi.python.org/pypi/cffi
.. _version of Gevent: https://github.com/schmir/gevent
