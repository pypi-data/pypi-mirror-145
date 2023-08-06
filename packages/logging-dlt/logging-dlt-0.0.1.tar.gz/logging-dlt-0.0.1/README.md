# logging-dlt

![coverage](https://gitlab.com/Menschel/logging-dlt/badges/master/coverage.svg)

[Documentation](https://menschel.gitlab.io/logging-dlt/)

[DLT Autosar Specification](https://www.autosar.org/fileadmin/user_upload/standards/classic/4-3/AUTOSAR_SWS_DiagnosticLogAndTrace.pdf)

A python logging adapter for "diagnostic log and trace" protocol.

# Description

The goal of this project is to provide a way to route the proprietary dlt
protocol into the python logging framework. This is done by using a logging adapter
together with a dlt stream parser.


# DLT protocol
DLT (Diagnostic Log and Trace) is a proprietary logging protocol.
It is used in debugging automotive ECUs that run Autosar OS.

You should NOT use it if you have the choice!

It has many traps, inconsistencies and architecture dependencies.
In the field it does overflow its own stream buffer, corrupting data on the wire.
It causes endianess problems, e.g. use big endian even if it announced little endian
a few bytes before (
[Proof 1](https://github.com/COVESA/dlt-daemon/blob/master/src/shared/dlt_common.c#L1034),
[2](https://github.com/COVESA/dlt-daemon/blob/master/src/shared/dlt_common.c#L846)
) etc.

It is clear that it did not compete against any other logging mechanism or had any trial phase.
It was just forged into a standard that is enforced for the Autosar OS.

