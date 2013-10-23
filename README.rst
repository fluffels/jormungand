==========
Jormungand
==========

Contents
========

1. Summary
2. Prerequisites
3. Roadmap
4. Process Model
5. Includes JSON Configurations
6. Description of Plugins

   1. Extraction

      1. SQLAlchemy Flat Storage Source

   2. Storage

      1. SQLALchemy Flat Storage

7. Description of API

   1. Data Model
   2. Extraction
   3. Normalisation
   4. Validation
   5. Storage


Summary
=======

Jormungand is a plugin-based framework for creating applications that extracting data from varied sources,
processing and validated the extracted data and then storing it again in a common format.

Jormungand defines a basic model for the process defined above and allows for specific implementations of various
stages in the process to be added or removed in a pluggable fashion.

Jormungand also provides a CLI script that is used to intiate the extraction post-process with a specified
configuration of plugins and input.


Prerequisites
=============

1. Python 2.7 or PyPy 2.1
2. Yapsy 1.9.2
3. SQLAlchemy 0.8.2 (OPTIONAL: Only required if you plan to use the SQLAlchemy Flat Storage plugin)


Roadmap
=======

The following features are planned:

1. CLI script for interacting with Jormungand (DONE)
2. Jormungand Plugin Manager (DONE)
3. DataModel API (DONE)
4. Extraction API (DONE)
5. Normalisation API (DONE)
6. Validation API (DONE)
7. Storage API (DONE)
8. Data Source API
9. Transposition API
10. Multi-processing support
11. Refactoring of CLI script and Jormungand Plugin Manager
12. GUI for interacting with Jormungand


Process Model
=============

Jormungand defines its basic process model as follows:

1. Data Model
2. Jormungand
3. Post-Processing
4. Validation
5. Storage


Includes JSON Configurations
============================

TBD


Description of Plugins
======================

TBD


Description of APIs
===================

TBD
