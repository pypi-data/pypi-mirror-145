The following 'class' layout should be followed as much as possible.

#Adapters
Adapters should be used for any cludges that fit one thing into another, for instance
- connecting S3 files into a streaming based class
- converting filters specific to an endpoint from one form to another
- adding headers to requests

#Handlers
Handlers should be used for logical datalake concepts, for instance
dealing with datasets or partitions in operational ways

#Providers
Providers are purely for injectors, to be used with inversion of control
with the Injector framework. 
There should be little to no auxiliary code or methods inside.

#Services
Services should provide some functionality addendum to the api,
for instance caching common calls, or analytics.
Use of services 'bare' by each repo should be kept to a minimum.
=

This folder is also used for abstract classes used by the other classes of the repo,
e.g. abstract_backend_handler_service -> s3_dataset_handler

Recall we want abstraction as much as possible, even though or services
are mostly aws based at the moment, this may change in the future.

