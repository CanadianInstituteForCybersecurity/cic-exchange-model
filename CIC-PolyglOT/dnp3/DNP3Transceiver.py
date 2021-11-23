import cmd
import logging
import sys
import time

from datetime import datetime
from pydnp3 import opendnp3, openpal
from dnp3.master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication
from dnp3.master import command_callback, restart_callback, RESULTS, SOE_RESULTS
import asyncio

stdout_stream = logging.StreamHandler(sys.stdout)
stdout_stream.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))

_log = logging.getLogger(__name__)
_log.addHandler(stdout_stream)
_log.setLevel(logging.DEBUG)


class DNP3Transceiver():
    """
    DNP3 Tranceiver receives a dict containing parameters which is used
    to query a DNP3 server for information
    """
    def __init__(self, outstation_address, outstation_id, comm_type):
        self.application = MyMaster(log_handler=MyLogger(),
                                    listener=AppChannelListener(),
                                    soe_handler=SOEHandler(),
                                    master_application=MasterApplication(),
                                    outstation_address=outstation_address,
                                    outstation_id=outstation_id,
                                    type=comm_type)

    def query(self, command_params):
        """This method is responsible for making queries to a DNP3 server"""
        if command_params["command"] == "direct_operate_binary":
            self.direct_operate_binary(command_params["start_index"], command_params["value"])
            while not RESULTS:
                pass
            while not self.application.values:
                pass
            return RESULTS, self.application.values
        elif command_params["command"] == "select_operate_binary":
            self.select_and_operate_binary(command_params["start_index"], command_params["value"])
            while not RESULTS:
                pass
            while not self.application.values:
                pass
            return RESULTS, self.application.values
        elif command_params["command"] == "read":
            self.do_scan_range(command_params["group_id"], command_params["variation"],
                               command_params["start_index"], command_params["stop_index"])
            while not self.application.values:
                pass
            return self.application.values
        elif command_params["command"] == "scan_objects":
            self.do_scan_objects(command_params["group_id"], command_params["variation"])
            while not self.application.values:
                pass
            return self.application.values
        elif command_params["command"] == "direct_operate_analog":
            self.direct_operate_analog(command_params["start_index"], command_params["value"])
            while not RESULTS:
                pass
            while not self.application.values:
                pass
            return RESULTS, self.application.values
        elif command_params["command"] == "select_operate_analog":
            self.select_and_operate_analog(command_params["start_index"], command_params["value"])
            while not RESULTS:
                pass
            while not self.application.values:
                pass
            return RESULTS, self.application.values
        elif command_params["command"] == "stop_unsolicited":
            self.do_disable_unsol()
            while not self.application.values:
                pass
            return self.application.values
        elif command_params["command"] == "actual_read":
            self.do_read_function(command_params["group_id"],command_params["variation"],command_params["count"])
            while not self.application.values:
                pass
            return self.application.values

    def do_disable_unsol(self):
        """Performs the function DISABLE_UNSOLICITED to the DNP3 server."""
        headers = [opendnp3.Header().AllObjects(60, 2),
                   opendnp3.Header().AllObjects(60, 3),
                   opendnp3.Header().AllObjects(60, 4)]
        self.application.master.PerformFunction("disable unsolicited",
                                                opendnp3.FunctionCode.DISABLE_UNSOLICITED,
                                                headers,
                                                opendnp3.TaskConfig().Default())

    def direct_operate_binary(self, start_index, value):
        """Sends a DirectOperate to a BinaryOutput of a DNP3 Server."""
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(value),
                                                     start_index,
                                                     command_callback)

    def select_and_operate_binary(self, start_index, value):
        """Sends a DirectOperate command to a BinaryOutput"""
        self.application.send_select_and_operate_command(opendnp3.ControlRelayOutputBlock(value),
                                                     start_index,
                                                     command_callback)

    def direct_operate_analog(self, start_index, value):
        """Sends a DirectOperate command to an AnalogOutput to the Outstation"""
        self.application.send_direct_operate_command(opendnp3.AnalogOutputInt32(value),
                                                     start_index,
                                                     command_callback)

    def select_and_operate_analog(self, start_index, value):
        """Sends a SelectOperate to an AnalogOutput of the Outstation."""
        self.application.send_select_and_operate_command(opendnp3.AnalogOutputInt32(value),
                                                         start_index,
                                                         command_callback)

    def do_restart(self):
        """Requests that the Outstation performs a cold restart."""
        self.application.master.Restart(opendnp3.RestartType.COLD, restart_callback)

    def do_scan_objects(self, group_id, variation):
        """Sends a command to ScanAllObjects of a Group and variation."""
        self.application.master.ScanAllObjects(opendnp3.GroupVariationID(group_id, variation),
                                               opendnp3.TaskConfig().Default())

    def do_scan_range(self, groupID, variation, startIndex, stopIndex):
        """Sends an ad-hoc scan of a range of points for a Group and variation"""
        self.application.master.ScanRange(opendnp3.GroupVariationID(groupID, variation), startIndex, stopIndex,
                                          opendnp3.TaskConfig().Default())

    def do_read_function(self, groupID, variation, count):
        """Sends a read command to an object with a particular group id and variation"""
        headers = [opendnp3.Header.Count16(groupID, variation, count)]
        self.application.master.PerformFunction("read input analog group 32",
                                                opendnp3.FunctionCode.READ,
                                                headers,
                                                opendnp3.TaskConfig().Default())

    def do_write_time(self):
        """Writes a TimeAndInterval to the Outstation"""
        millis_since_epoch = int((datetime.now() - datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
        self.application.master.Write(opendnp3.TimeAndInterval(opendnp3.DNPTime(millis_since_epoch),
                                                               100,
                                                               opendnp3.IntervalUnits.Seconds),
                                      0,  # index
                                      opendnp3.TaskConfig().Default())

    def do_quit(self):
        """Shutdown the master client"""
        self.application.shutdown()
        exit()


def execute_command(outstation_address, outstation_id, comm_type, recv_queue, send_queue):
    """Creates the DNP3Tranceiver object and receives request commands from the
    a recipient queue and sends the response to a sender queue
    """
    dnp3tx = DNP3Transceiver(outstation_address=outstation_address, outstation_id=outstation_id, comm_type=comm_type)
    command = recv_queue.get()
    result = dnp3tx.query(command)
    while not result:
        pass
    send_queue.put(result)
    dnp3tx.do_quit()
    del dnp3tx