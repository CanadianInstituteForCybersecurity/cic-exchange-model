from modbus import ModbusCommandSTIX
from stix2 import properties
from stix2 import CustomObject

@CustomObject('modbus-tcp', [
    ('host', properties.StringProperty(required=True)),
    ('unit_id_hex', properties.IntegerProperty(min=0,max=255)),
    ('pdu', properties.STIXObjectProperty(ModbusCommandSTIX.ModbusCommand))
])

class ModbusTCP(object):
        def __init__(self, host, unit_id_hex, **kwargs):
            if host and (host == "" or not host):
                raise ValueError("the value for host is invalid")