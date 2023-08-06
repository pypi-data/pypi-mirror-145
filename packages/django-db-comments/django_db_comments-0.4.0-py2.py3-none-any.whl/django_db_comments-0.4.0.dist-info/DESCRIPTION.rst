=============================
Django Db Comments
=============================

.. image:: https://badge.fury.io/py/django-db-comments.svg
    :target: https://badge.fury.io/py/django-db-comments

.. image:: https://travis-ci.org/vanadium23/django-db-comments.svg?branch=master
    :target: https://travis-ci.org/vanadium23/django-db-comments

.. image:: https://codecov.io/gh/vanadium23/django-db-comments/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/vanadium23/django-db-comments

Move your model's verbose name and help_text to database comments:

.. image:: setup-and-result.jpg
    :alt: Add to INSTALLED_APPS and see description in database.

Documentation
-------------

The full documentation is at https://django-db-comments.readthedocs.io.

Quickstart
----------

Install Django Db Comments::

    pip install django-db-comments

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_db_comments',
        ...
    )

Features
--------

* Copy verbose_name and help_text to columns in DB, currently: Postgres_.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _Postgres: https://www.postgresql.org/docs/9.1/sql-comment.html




History
-------

0.4.0 (2022-04-02)
++++++++++++++++++

* Skip proxy, abstract and not managed model. (Issue #11 by @xjlin0)

0.3.1 (2021-08-02)
++++++++++++++++++

* Update meta information in setup.py.

0.3.0 (2021-08-02)
++++++++++++++++++

* Add comments to tables based on verbose_name of model. (PR #5 by @ssatoh17)

0.2.2 (2019-05-19)
++++++++++++++++++

* Add psqlextra.backend to ALLOWED_ENGINES. (PR #4 by @shuribuzz)

0.2.1 (2019-05-19)
++++++++++++++++++

* Fix case, when help_text or verbose_name use ugettext_lazy from django. (PR #1 by @ErhoSen)


0.2.0 (2019-05-07)
++++++++++++++++++

* First release on PyPI.


