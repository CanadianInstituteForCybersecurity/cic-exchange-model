from iec61850 import iec61850

class GOOSETransceiver:
    def __init__(self, app_id, vlan_id, priority, address, interface="ens160"):
        self._comm_parameters = iec61850.CommParameters()
        self._comm_parameters.appId = app_id
        self._comm_parameters.dstAddress.append(address[0])
        self._comm_parameters.dstAddress.append(address[1])
        self._comm_parameters.dstAddress.append(address[2])
        self._comm_parameters.dstAddress.append(address[3])
        self._comm_parameters.dstAddress.append(address[4])
        self._comm_parameters.dstAddress.append(address[5])
        self._comm_parameters.vlanId = vlan_id
        self._comm_parameters.vlanPriority = priority
        self._publisher = iec61850.GoosePublisher_create(self._comm_parameters, interface)

    def query(self):
        dataset_values = iec61850.LinkedList_create()
        iec61850.LinkedList_add(dataset_values, iec61850.MmsValue_newIntegerFromInt32(1234))

        if self._publisher:
            iec61850.GoosePublisher_setGoCbRef(self._publisher, "simpleIOGenericIO/LLN0$GO$gcbAnalogValues");
            iec61850.GoosePublisher_setConfRev(self._publisher, 1);
            iec61850.GoosePublisher_setDataSetRef(self._publisher, "simpleIOGenericIO/LLN0$AnalogValues");
            iec61850.GoosePublisher_setTimeAllowedToLive(self._publisher, 500);
            try:
                iec61850.GoosePublisher_publish(self._publisher, dataset_values);
            except:
                print("Error sending message")

            iec61850.GoosePublisher_destroy(self._publisher)
        else:
            print("Failed to create GOOSE publisher. "
                  "Reason can be that the Ethernet interface doesn't exist or root permission are required")

        iec61850.LinkedList_destroyDeep(dataset_values, iec61850.MmsValue_delete)

address = [0x01, 0x0c, 0xcd, 0x01, 0x00, 0x01]
goose_tx = GOOSETransceiver(app_id=1000, vlan_id=4, priority=4, address=address)
goose_tx.query()