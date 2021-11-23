from dnp3 import DNP3CommandSTIX
from stix2 import properties
from stix2 import CustomObject

@CustomObject('dnp3', [
    ('host', properties.StringProperty(required=True)),
    ('comm_type', properties.StringProperty(required=True)),
    ('outstation_id', properties.IntegerProperty(min=0, max=65535)),
    ('command_params', properties.STIXObjectProperty(DNP3CommandSTIX.DNP3Command))
])

class DNP3Frame(object):
        def __init__(self, host, comm_type, outstation_id, **kwargs):
            if (host and host == "") or not host:
                raise ValueError("the value for host is invalid")
            if (comm_type and comm_type == "") or not comm_type:
                raise ValueError("the value for comm_type is invalid")
