# Installation Instructions
1. Run a python virtual environment
2. Install [flask](https://pypi.org/project/Flask/), [pydnp3](https://pypi.org/project/pyopendnp3/) and [modbus-tk](https://pypi.org/project/modbus_tk/).
3. Run STIXFieldMapper.py

# Folder Structure
* STIXFieldMapper.py
    * It is the main entry point for the application
    * It receives requests from TAXII client and calls the appropriate FieldBus Transceiver based on the custom STIX object received
    * Returns the results received from a Transceiver to the TAXII client.
* modbus
    * Contains the ModbusTransceiver
* dnp3
    * Contains the DNP3Transceiver
* iec61850
    * goose
        * Contains GOOSETransceiver (currently not functioning)
    * mms
        * Contains MMSTransceiver
    * iec61850.py, iec61850.so
        * They are python bindings for [libiec61850](https://github.com/mz-automation/libiec61850). They must be included for the MMSTransceiver and GOOSETransceiver to work.