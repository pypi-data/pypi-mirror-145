# diematic_client

A Python module to consume information from diematic-server.

## Software requirements

 * A running instance of diematic-server. In my case I've it running in a Raspberry PI 3 connected to the DeDietrich boiler using the RS-485 port. See the documentation for the diematic-server repository

The documentation for the diematic-server project is in a separate repository and it is also a pipy package available to download and use.

This package has been created to isolate the functionality to access to the server and allow for the integration of components inside home assistant.

## Installation

```
pip install diematic_client
```

If you are installing the home assistant components (At this time, they are WIP) they should install this package automatically

## References

This project has been created following the original structure of the IPP printer module
