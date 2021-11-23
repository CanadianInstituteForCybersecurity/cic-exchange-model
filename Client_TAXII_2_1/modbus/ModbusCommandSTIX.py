from stix2 import properties
from stix2 import CustomObject

@CustomObject('modbus-command-frame', [
    ('function_code_hex', properties.IntegerProperty(required=True, min=0, max=255)),
    ('address_hex', properties.IntegerProperty(min=0, max=65535)),
    ('quantity_hex', properties.IntegerProperty(min=0, max=65280)),
    ('value_hex', properties.IntegerProperty(min=0, max=65535)),
])
class ModbusCommand(object):
    def __init__(self, **kwargs):
        pass