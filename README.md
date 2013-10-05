Jormungand
==========

Jormungand is a plugin-based framework for creating applications that extracting data from varied sources,
processing and validated the extracted data and then storing it again in a common format.

Jormungand defines a basic model for the process defined above and allows for specific implementations of various
stages in the process to be added or removed in a pluggable fashion.

Jormungand also provides a CLI script that is used to intiate the extraction post-process with a specified
configuration of plugins and input.


The Jormungand Process Model
-------------------------

Jormungand defines its basic process model as follows:

1. Data Model
2. Jormungand
3. Post-Processing
4. Validation
5. Storage