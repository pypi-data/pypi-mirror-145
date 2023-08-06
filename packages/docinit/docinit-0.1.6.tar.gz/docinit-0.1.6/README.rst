|Build| |PyPI|

DocInit
=======

DocInit is an opiniated, yet flexible documentation generator for your Python projects.
It removes the burden of rewriting the same configuration files over and over, and instead favors a simple, non-repetitive declarative style. It uses `Sphinx <https://www.sphinx-doc.org/>`__ and `Sphinx AutoAPI <https://github.com/readthedocs/sphinx-autoapi>`__ behind the scenes.

Features
--------

- Entirely configurable from your `setup.cfg` file
- Automatically fills the blanks so you don't have to repeat yourself
- Allows master and sub projects
- Compatible with `Read the Docs <https://readthedocs.org/>`__
- Flexible and extensible

Example
-------

The `Timeflux documentation <https://doc.timeflux.io>`__ is managed by DocInit.

Install
-------

.. code::

    pip install docinit

Usage
-----

Write your documentation
~~~~~~~~~~~~~~~~~~~~~~~~

Or not. If you don't do anything, DocInit will automatically find your packages, generate API documentation, and create an index page (using either your repo's `README.rst` file or a default paragraph).

You can add your own `.rst` files in the `doc` directory, and overwrite the default `index.rst`. Put your logo and favicon in `doc/_static/logo.png` and `doc/_static/favicon.ico`, respectively.

If you need to configure further, do it in the ``docinit`` section of your `setup.cfg <https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files>`__. Refer to the `Configuration`_ section for details.

Setup a Sphinx project
~~~~~~~~~~~~~~~~~~~~~~

The following will take care of initializing everything:

.. code::

    python setup.py docinit

If you don't have a `setup.py` file, you can instead simply run:

.. code::

    docinit

Don't worry, nothing will be overwritten if a file with the same name already exists. There is no need to re-run this command, even if you modify your `setup.cfg`. But if you do, nothing bad will happen.

You don't have to commit the generated files. Refer to the `Read the Docs`_ section to learn how to setup your project at build time.

Build
~~~~~

.. code::

    cd doc
    make html

You can now find your generated documentation in `doc/_build/html/`.

By default, the `make` command will return an error (but will still build everything) in case of warning. This allows for easy integration in your CI/CD pipelines.

Configuration
-------------

The following options are accepted:

================= ====
Key               Type
================= ====
``doc_dir``       str
``name``          str
``parent_url``    str
``logo_url``      str
``favicon_url``   str
``version``       str
``release``       str
``packages``      list
``author``        str
``copyright``     str
``analytics``     str
``canonical_url`` str
================= ====

There is no required option. If not set, DocInit will try to find an appropriate value elsewhere. If it fails, it will settle on a default value.

doc_dir
~~~~~~~

This is where your documentation lives.

======= =======
Default Lookups
======= =======
``doc`` - ``source-dir`` in the ``build_sphinx`` section
======= =======

name
~~~~

The name of your project.

=========== =======
Default     Lookups
=========== =======
``Project`` - ``project`` in the ``build_sphinx`` section
            - ``name`` in the ``metadata`` section
            - name of the current git repo
=========== =======

parent_url
~~~~~~~~~~

If you are managing a `subproject <https://docs.readthedocs.io/en/stable/subprojects.html>`__, this is the URL of the main project. When set, DocInit adds a `Back` entry in the menu, and configures the `intersphinx mapping <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`__.

======== =======
Default  Lookups
======== =======
``None``
======== =======

logo_url
~~~~~~~~

The URL of an image that will be downloaded to `doc/_static/logo.png`. Useful for subprojects.

======== =======
Default  Lookups
======== =======
``None``
======== =======

favicon_url
~~~~~~~~~~~

The URL of an image that will be downloaded to `doc/_static/favicon.ico`. Useful for subprojects.

======== =======
Default  Lookups
======== =======
``None``
======== =======

version
~~~~~~~

The `semantic version <https://semver.org/>`__ of your package. If it is not explicitly defined, DocInit will use `setuptools_scm <https://github.com/pypa/setuptools_scm>`__ to fetch it from git tags, or fallback to ``0.0.0``.

============== =======
Default        Lookups
============== =======
From git tags  - ``version`` in the ``build_sphinx`` section
               - ``version`` in the ``metadata`` section
============== =======

release
~~~~~~~

The full version of your package, including VCS status. If it is not explicitly defined, DocInit will use `setuptools_scm <https://github.com/pypa/setuptools_scm>`__ to fetch it from git tags, or fallback to ``0.0.0``.

============== =======
Default        Lookups
============== =======
From git tags  - ``release`` in the ``build_sphinx`` section
============== =======

packages
~~~~~~~~

The list of packages for which the API documentation will be generated. If it is not specified, DocInit will discover packages from the root of your project (where `setup.cfg` is located).

========= =======
Default   Lookups
========= =======
``find:`` - ``packages`` in the ``options`` section
========= =======

author
~~~~~~

The author of the project.

============= =======
Default        Lookups
============= =======
``Anonymous``  - ``author`` in the ``metadata`` section
               - From the first commit in the current git repository
============= =======

copyright
~~~~~~~~~

The copyright for this project. If it is not defined, it will be constructed from the year of the first commit, the current year, and ``author``.

========== =======
Default    Lookups
========== =======
Generated  - ``copyright`` in the ``build_sphinx`` section
========== =======

analytics
~~~~~~~~~

Your Google Analytics ID. It should look like ``UA-XXXXXXX-1``.

======== =======
Default  Lookups
======== =======
``None``
======== =======

canonical_url
~~~~~~~~~~~~~

If your URL is available through multiple URLs, the canonical url indicates to search engines which one it should index. The URL points to the root path of the documentation and requires a trailing slash.

======== =======
Default  Lookups
======== =======
``None``
======== =======

Arbitrary options
~~~~~~~~~~~~~~~~~

That is not all: you can pass arbitrary options, and they will be injected in `conf.py`. For example, setting: ``autoapi_generate_api_docs = 0`` will disable API documentation. Please refer to the official `Sphinx <https://www.sphinx-doc.org/en/master/usage/configuration.html>`__ and `Sphinx AutoAPI <https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html>`__ documentation for recognized options.

Read the docs
-------------

If you decide to not push the files created by DocInit, the easiest way is to install your package before building the docs. You can configure this behavior either in the `Advanced settings` tab of your dashboard or in your `configuration file <https://docs.readthedocs.io/en/stable/config-file/v2.html#packages>`__.

Then you just need to invoke DocInit during the setup process.

This can be achieved in your `setup.py`:

.. code:: python

    setup(
        ...
        setup_requires="docinit",
        docinit=True,
        ...
    )

Or if you prefer, in your `pyproject.toml`:

.. code:: toml

    [tool.docinit]

    [build-system]
    requires = ["setuptools>=42", "wheel", "docinit"]
    build-backend = "setuptools.build_meta"

Please note: before version `20.1.b1` and since version `20.1.1`, `pip` `builds in a temporary directory <https://pip.pypa.io/en/stable/news/>`__. Therefore, on `Read The Docs` you need to install the package with `setup.py` so the documentation is generated in the current directory.


Alternative build systems
-------------------------

DocInit currently only parses Setuptools `setup.cfg` files. We plan to add support for other build systems as well, such as `Flit <https://flit.readthedocs.io/>`__ and `Poetry <https://python-poetry.org/>`__, which rely on `pyproject.toml` files.


.. |Build| image:: https://github.com/mesca/docinit/workflows/Python%20application/badge.svg
.. |PyPI| image:: https://badge.fury.io/py/docinit.svg
