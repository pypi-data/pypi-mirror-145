Informatics Matters OpenAPI Validator (oval)
============================================

.. image:: https://badge.fury.io/py/im-openapi-validator.svg
   :target: https://badge.fury.io/py/im-openapi-validator
   :alt: PyPI package (latest)

A utility designed as a `pre-commit`_ OpenAPI file validator::

    oval --help

Use it by adding it to your repository's ``.pre-commit-config.yaml`` file::

    # Basic OpenAPI Validator
    - repo: https://github.com/informaticsmatters/openapi-validator
      rev: '1.0.0'
      hooks:
      - id: im-oval
        files: app/openapi/openapi.yaml

.. _pre-commit: https://pre-commit.com

Installation
============

The OpenAPI validator is published on `PyPI`_ and can be installed from there::

    pip install im-openapi-validator

This is a Python 3 utility, so try to run it from a recent (ideally 3.10)
Python environment.

.. _PyPI: https://pypi.org/project/im-openapi-validator/

Get in touch
------------

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/openapi-validator
