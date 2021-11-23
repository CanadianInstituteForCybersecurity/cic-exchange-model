from stix2 import properties
from stix2 import CustomObject

@CustomObject('mms-command-frame', [
    ('command', properties.StringProperty(required=True)),
    ('logical_device', properties.StringProperty()),
    ('logical_node', properties.StringProperty()),
    ('data_object', properties.StringProperty()),
    ("data_reference_attribute", properties.StringProperty()),
    ('value', properties.FloatProperty()),
    ('functional_constraint', properties.IntegerProperty()),
])
class MMSCommand(object):
        def __init__(self, command=None, logical_device=None, logical_node=None,
                     data_object=None,data_reference_attribute=None,value=None,**kwargs):
            if command == "" and command:
                raise ValueError("the value for command is invalid")
            if logical_device and logical_device == "":
                raise ValueError("the value for logical device is invalid")
            if data_object and data_object == "":
                raise ValueError("the value for data object is invalid")
            if logical_node and logical_node == "":
                raise ValueError("the value for logical node is invalid")
            if data_reference_attribute and data_reference_attribute == "":
                raise ValueError("the value for data reference attribute is invalid")