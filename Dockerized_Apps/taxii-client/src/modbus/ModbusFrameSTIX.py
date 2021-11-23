from modbus import ModbusCommandSTIX
from stix2 import properties
from stix2 import CustomObject

@CustomObject('modbus', [
    ('host', properties.StringProperty(required=True)),
    ('comm_type', properties.StringProperty()),
    ('unit_id_hex', properties.IntegerProperty(min=0, max=255)),
    ('command_params', properties.STIXObjectProperty(ModbusCommandSTIX.ModbusCommand))
])

class ModbusFrame(object):
        def __init__(self, host, comm_type, **kwargs):
            if host and (host == "" or not host):
                raise ValueError("the value for host is invalid")
            if comm_type and (comm_type == "" or not comm_type):
                raise ValueError("the value for host is invalid")