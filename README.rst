toscinterface
=============

A simple package to receive and store OSC-messages in python.

Thus far the package contains only one class which creates an OscInterface object. An OscInterface object is basically
a UDP-Socket with extended functionality to save received messages and to communicate with TouchOSC. This way, any
device running TouchOSC can be used as an input device to control python-programs or record data entries.

In theory, OSC messages sent by any program or device can be received, but the package is specifically designed around
the functionality and properties of TouchOSC. Using this package in a different context may not work as intended.

Download TouchOSC here: https://hexler.net/touchosc

toscinterface is developed on Windows 11. Compatibility with other operating systems is not
tested.