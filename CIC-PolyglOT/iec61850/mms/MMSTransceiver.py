from iec61850 import iec61850


class MMSTransceiver():
    def __init__(self, hostname, port):
        self._hostname = hostname
        self._port = port
        self._con = iec61850.IedConnection_create()

    def connect(self):
        err = iec61850.IedConnection_connect(self._con, self._hostname, self._port)
        return err

    def query(self, command_params):
        err = self.connect()
        if err == iec61850.IED_ERROR_OK:
            if command_params["command"] == "getLogicalDeviceList":
                response = self.getLogicalDeviceList()
                return response

            if command_params["command"] == "getLogicalDeviceDirectory":
                response = self.getLogicalDeviceDirectory(command_params["logical_device"])
                return response
            if command_params["command"] == "getLogicalNodeVariables":
                response = self.getLogicalNodeVariables(command_params["logical_node"])
                return response
            if command_params["command"] == "getLogicalDeviceDataSets":
                response = self.getLogicalDeviceDataSets(command_params["logical_device"])
                return response
            if command_params["command"] == "getDataValues":
                response = self.getDataValues(command_params['functional_constraint'],
                                              command_params['data_reference_attribute'])
                return response
            if command_params["command"] == "setDataValues":
                response = self.setDataValues(command_params['functional_constraint'],
                                              command_params['data_reference_attribute'], command_params["value"])
                return response
        else:
            return f"Error connecting to server. Error code: {err}"

    def getLogicalDeviceList(self):
        """Executes GetLogicalDeviceList command to MMS Server"""
        logical_device_list = []
        [devices, error] = iec61850.IedConnection_getLogicalDeviceList(self._con)
        device = iec61850.LinkedList_getNext(devices)
        while device:
            logical_device_name = iec61850.toCharP(device.data)
            logical_device_list.append(logical_device_name)
            device = iec61850.LinkedList_getNext(device)
        iec61850.LinkedList_destroy(devices)
        iec61850.IedConnection_destroy(self._con)
        return logical_device_list

    def getLogicalDeviceDirectory(self, logical_device):
        """Executes GetLogicalDeviceDirectory command to MMS Server"""
        logical_nodes_list = []
        [logicalNodes, error] = iec61850.IedConnection_getLogicalDeviceDirectory(self._con, logical_device)
        logical_node = iec61850.LinkedList_getNext(logicalNodes)
        while logical_node:
            logical_node_name = iec61850.toCharP(logical_node.data)
            logical_nodes_list.append(logical_node_name)
            logical_node = iec61850.LinkedList_getNext(logical_node)
        iec61850.LinkedList_destroy(logicalNodes)
        iec61850.IedConnection_destroy(self._con)
        return logical_nodes_list

    def getLogicalNodeVariables(self, logical_node):
        """Executes GetLogicalNodeVariables to the MMS Server"""
        data_object_list = []
        [data_objects, error] = iec61850.IedConnection_getLogicalNodeVariables(self._con, logical_node)
        data_object = iec61850.LinkedList_getNext(data_objects)
        while data_object:
            data_object_name = iec61850.toCharP(data_object.data)
            data_object_list.append(data_object_name)
            data_object = iec61850.LinkedList_getNext(data_object)
        iec61850.LinkedList_destroy(data_objects)
        iec61850.IedConnection_destroy(self._con)
        return data_object_list

    def getLogicalDeviceDataSets(self, logical_device):
        """Executes GetLogicalDeviceDataSets to the MMS Server"""
        dataset_list = []
        [datasets, error] = iec61850.IedConnection_getLogicalDeviceDataSets(self._con, logical_device)
        dataset = iec61850.LinkedList_getNext(datasets)
        while dataset:
            dataset_name = iec61850.toCharP(dataset)
            dataset_list.append(dataset_name)
            dataset = iec61850.LinkedList_getNext(dataset)
        iec61850.LinkedList_destroy(datasets)
        iec61850.IedConnection_destroy(self._con)
        return dataset_list

    def getDataValues(self, functional_constraint, data_ref_attribute):
        """Executes GetDataValues to the MMS Server"""
        value = iec61850.IedConnection_readFloatValue(self._con, data_ref_attribute, functional_constraint)
        return value

    def setDataValues(self, functional_constraint, data_ref_attribute, value):
        """Executes SetDataValues to the MMS Server"""
        status = iec61850.IedConnection_writeFloatValue(self._con, data_ref_attribute, functional_constraint,
                                                        value)
        return status
