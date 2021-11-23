from modbus import ModbusCommandSTIX
from stix2 import properties
from stix2 import CustomObject

@CustomObject('modbus-rtu', [
    ('host', properties.StringProperty(required=True)),
    ('unit_id_hex', properties.IntegerProperty(min=0, max=255)),
    ('pdu', properties.STIXObjectProperty(ModbusCommandSTIX.ModbusCommand))
])

class ModbusRTU(object):
        def __init__(self, host, unit_id_hex, **kwargs):
            if host and (host == "" or not host):
                raise ValueError("the value for host is invalid")


#print("*********************************************************************")
#print("Example of MODBUS TCP object")
#print("*********************************************************************")
# pdu = ModbusPDUSTIX.PDU(function_code_hex=6,
#                         address_hex=12, value_hex=8593)
#
# obj1 = ModbusRTU (host="/dev/ttyS14", unit_id_hex=1,
#                   pdu= pdu)
# print(obj1)