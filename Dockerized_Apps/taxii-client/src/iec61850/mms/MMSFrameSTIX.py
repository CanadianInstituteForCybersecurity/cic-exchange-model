from iec61850.mms import MMSCommandSTIX
from stix2 import properties
from stix2 import CustomObject


@CustomObject('mms', [
    ('host', properties.StringProperty(required=True)),
    ('command_params', properties.STIXObjectProperty(MMSCommandSTIX.MMSCommand))
])
class MMSFrame(object):
    def __init__(self, host, **kwargs):
        if (host and host == "") or not host:
            raise ValueError("the value for host is invalid")

