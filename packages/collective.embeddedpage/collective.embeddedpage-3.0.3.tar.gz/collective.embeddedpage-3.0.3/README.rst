.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.embeddedpage
==============================================================================

.. image:: https://github.com/collective/collective.embeddedpage/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/collective/collective.embeddedpage/actions/workflows/ci.yml

.. image:: https://img.shields.io/pypi/status/collective.embeddedpage.svg
    :target: https://pypi.python.org/pypi/collective.embeddedpage/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/collective.embeddedpage.svg
    :target: https://pypi.python.org/pypi/collective.embeddedpage
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/collective.embeddedpage.svg
    :target: https://pypi.python.org/pypi/collective.embeddedpage
    :alt: License

|

.. image:: https://raw.githubusercontent.com/collective/collective.embeddedpage/main/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

collective.embeddedpage allows to embed remote HTML pages in Plone.

Features
--------

- Adds EmbeddedPage content types (Dexterity based)
- Displays remote HTML within the view of the EmbeddedPage content object


Examples
--------

This add-on can be seen in action at the following sites:

- `Humboldt-Universität zu Berlin`_.


Translations
------------

This product has been translated into

- German


Installation
------------

Add collective.embeddedpage in your Plone installation with ``pip install collective.embeddedpage``


Local Development
-----------------

Clone this repository::

    git clone git@github.com:collective/collective.embeddedpage.git


Install Plone and this package::

    cd collective.embeddedpage
    make build-plone-6

Run tests::

    make test


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.embeddedpage/issues
- Source Code: https://github.com/collective/collective.embeddedpage


Support
-------

If you are having issues,
`please let us know <https://github.com/collective/collective.embeddedpage/issues>`_.

If you require professional support, feel free to drop us a note at info@kitconcept.com.


Credits
-------

.. image:: https://www.hu-berlin.de/++resource++humboldt.logo.Logo.png
   :width: 200px
   :alt: HU Berlin
   :target: https://www.hu-berlin.de

|

.. image:: https://github.com/collective/collective.embeddedpage/raw/main/fzj-logo.jpeg
   :width: 200px
   :alt: Forschungszentrum Jülich
   :target: https://www.fz-juelich.de

|

The development of this plugin has been kindly sponsored by `Humboldt-Universität zu Berlin`_ and `Forschungszentrum Jülich`_.

|

.. image:: https://raw.githubusercontent.com/collective/collective.embeddedpage/main/kitconcept.png
   :width: 200px
   :alt: kitconcept
   :target: https://kitconcept.com/

Developed by `kitconcept`_.


License
-------

The project is licensed under the GPLv2.

.. _Humboldt-Universität zu Berlin: https://www.hu-berlin.de
.. _Forschungszentrum Jülich: https://www.fz-juelich.de
.. _kitconcept: http://www.kitconcept.com/
