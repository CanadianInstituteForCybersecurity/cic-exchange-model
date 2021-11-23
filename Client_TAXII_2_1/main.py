import time
import os

from iec61850.mms import MMSCommandSTIX
from iec61850.mms import MMSFrameSTIX
from taxii.TaxiiTransceiver import TaxiiTransceiver
from dnp3 import DNP3FrameSTIX, DNP3CommandSTIX
from modbus import ModbusFrameSTIX, ModbusCommandSTIX


#get TAXII Server settings from ENV
user_name = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
taxii_server_address = os.environ.get('TAXII_SERVER_ADDRESS')
taxii_server_port = os.environ.get('TAXII_SERVER_PORT')
taxii_api_root = os.environ.get('TAXII_API_ROOT')
taxii_collection = os.environ.get('TAXII_COLLECTION')
taxii_url = "http://" + taxii_server_address + ":" + taxii_server_port + "/" + taxii_api_root + "/"
t_xceiver = TaxiiTransceiver(url=taxii_url, username=user_name, user_password=password)

#get CIC-PolyglOT settings from ENV
dxl_address = os.environ.get('DXL_ADDRESS')
dxl_port = os.environ.get('DXL_PORT')
dxl_method = os.environ.get('DXL_METHOD')
dxl_url = "http://" + dxl_address + ":" + dxl_port + "/" + dxl_method

#================================Modbus=========================
#create STIX objects for Modbus RTU and add it to the TAXII server
for i in range(1,6):
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=6, address_hex=(i*4), value_hex=(12*i))
    modbus_rtu = ModbusFrameSTIX.ModbusFrame (host="/dev/ttyS0", comm_type="rtu", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_rtu)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=3, address_hex=(i * 9), quantity_hex=(6 * i))
    modbus_rtu = ModbusFrameSTIX.ModbusFrame (host="/dev/ttyS0", comm_type="rtu", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_rtu)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=5, address_hex=(i * 4), value_hex=(12 * i))
    modbus_rtu = ModbusFrameSTIX.ModbusFrame (host="/dev/ttyS0", comm_type="rtu", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_rtu)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=1, address_hex=(i * 9), quantity_hex=(6 * i))
    modbus_rtu = ModbusFrameSTIX.ModbusFrame (host="/dev/ttyS0", comm_type="rtu", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_rtu)

#create STIX objects for Modbus TCP and add it to the TAXII server
for i in range(1,6):
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=6, address_hex=(i*4), value_hex=(12*i))
    modbus_tcp = ModbusFrameSTIX.ModbusFrame (host="127.0.0.1", comm_type="tcp", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id=taxii_collection, object=modbus_tcp)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=3, address_hex=(i * 9), quantity_hex=(6 * i))
    modbus_tcp = ModbusFrameSTIX.ModbusFrame (host="127.0.0.1", comm_type="tcp", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_tcp)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=5, address_hex=(i * 4), value_hex=(12 * i))
    modbus_tcp = ModbusFrameSTIX.ModbusFrame (host="127.0.0.1", comm_type="tcp", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_tcp)
    modbus_pdu = ModbusCommandSTIX.ModbusCommand(function_code_hex=1, address_hex=(i * 9), quantity_hex=(6 * i))
    modbus_tcp = ModbusFrameSTIX.ModbusFrame (host="127.0.0.1", comm_type="tcp", unit_id_hex=1, command_params=modbus_pdu)
    t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=modbus_tcp)


#============================DNP3=======================================================
#create STIX objects for DNP3 TCP and add it to the TAXII server
dnp3_command = DNP3CommandSTIX.DNP3Command(command="scan_objects", group_id=10, variation=1)
dnp3frame = DNP3FrameSTIX.DNP3Frame(host="127.0.0.1", comm_type="tcp",
                                    outstation_id=1024, command_params=dnp3_command)
t_xceiver.add_single_object(collection_id=taxii_collection, object=dnp3frame)

#create STIX objects for DNP3 Serial and add it to the TAXII server
dnp3_command = DNP3CommandSTIX.DNP3Command(command="scan_objects", group_id=10, variation=1)
dnp3frame = DNP3FrameSTIX.DNP3Frame(host="/dev/ttyS1", comm_type="serial",
                                    outstation_id=1024, command_params=dnp3_command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=dnp3frame)


#======================MMS==================================
#create STIX objects for IEC61850 MMS and add it to the TAXII server
command = MMSCommandSTIX.MMSCommand(command="getLogicalDeviceDirectory",logical_device="testmodelSENSORS")
mmsframe = MMSFrameSTIX.MMSFrame(host="127.0.0.1",command_params=command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=mmsframe)

command = MMSCommandSTIX.MMSCommand(command="getDataValues", data_reference_attribute="testmodelSENSORS/TTMP1.TmpSp.setMag.f",
                                   functional_constraint=2)
mmsframe = MMSFrameSTIX.MMSFrame(host="127.0.0.1", command_params=command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=mmsframe)

command = MMSCommandSTIX.MMSCommand(command="setDataValues", data_reference_attribute="testmodelSENSORS/TTMP1.TmpSp.setMag.f",
                                   functional_constraint=2, value=10.3)
mmsframe = MMSFrameSTIX.MMSFrame(host="127.0.0.1", command_params=command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=mmsframe)

command = MMSCommandSTIX.MMSCommand(command="getDataValues", data_reference_attribute="testmodelSENSORS/TTMP1.TmpSp.setMag.f",
                                   functional_constraint=2)
mmsframe = MMSFrameSTIX.MMSFrame(host="127.0.0.1", command_params=command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=mmsframe)

command = MMSCommandSTIX.MMSCommand(command="getLogicalNodeVariables", logical_node="testmodelSENSORS/TTMP1")
mmsframe = MMSFrameSTIX.MMSFrame(host="127.0.0.1", command_params=command)
t_xceiver.add_single_object(collection_id="91a7b528-80eb-42ed-a74d-c6fbd5a26116", object=mmsframe)

#retrieve all objects from the taxii collection
objects = t_xceiver.get_objects(collection_id=taxii_collection)


# pprint(objects)
object_ids = []

#sift obtain only custom STIX objects for OT
for obj in objects:
    if obj["type"] == "modbus":
        object_ids.append(obj["id"])
    if obj["type"] == "dnp3":
        object_ids.append(obj["id"])
    if obj["type"] == "mms":
        object_ids.append(obj["id"])

#Query CIC-PolyglOT for each object
for obj_id in object_ids:
    print(f'Retrieving {obj_id} from TAXII Server...')
    t_xceiver.get_single_object(collection_id=taxii_collection, object_id=obj_id)
    print(f'Querying {obj_id} from CIC-DXL...')
    t_xceiver.query_dxl(url=dxl_url)
    time.sleep(4)
