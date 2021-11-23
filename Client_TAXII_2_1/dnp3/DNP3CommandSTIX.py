from stix2 import properties
from stix2 import CustomObject

@CustomObject('dnp3-command-frame', [
    ('command', properties.StringProperty(required=True)),
    ('group_id', properties.IntegerProperty(min=0, max=255)),
    ('variation', properties.IntegerProperty(min=1, max=8)),
    ('start_index', properties.IntegerProperty(min=0, max=65535)),
    ('stop_index', properties.IntegerProperty(min=0, max=65535)),
    ('value', properties.IntegerProperty(min=0, max=65535)),
    ('count', properties.IntegerProperty(min=0, max=65535)),
])
class DNP3Command(object):
        def __init__(self, command=None, **kwargs):
            if command == "" or not command:
                raise ValueError("the value for command is invalid")