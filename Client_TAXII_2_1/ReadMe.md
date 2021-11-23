# Description
This folder contains code to query the TAXII and DXL servers. It uses TAXII and STIX version 2.1


# Installation Instructions
1. Run a python virtual environment
2. Install [taxii2client](https://pypi.org/project/taxii2-client/) and [stix2](https://pypi.org/project/stix2/)
3. Run main.py (run it only after setting up and running the TAXII server and CIC-PolyglOT)

# Folder Structure

* main.py
    * It is the entry point of the application
    * It creates custom STIX objects for DNP3, Modbus and MMS and adds it to a collection in a TAXII server, retrieves the objects again and querys the IoT-OT DXL server for information about those objects
* dnp3
    * Contains custom STIX objects for DNP3
* iec61850/mms
    * Contains custom STIX objects for MMS
* modbus
    * Contains custom STIX objects for Modbus
* taxii
    * Contains TAXIITransceiver