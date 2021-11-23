import logging
import sys
import time

from pydnp3 import opendnp3, openpal, asiopal, asiodnp3
from dnp3.visitors import *

FILTERS = opendnp3.levels.NORMAL | opendnp3.levels.ALL_COMMS
HOST = "127.0.0.1"
LOCAL = "0.0.0.0"
PORT = 20000

RESULTS = []
SOE_RESULTS = []
stdout_stream = logging.StreamHandler(sys.stdout)
stdout_stream.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))

_log = logging.getLogger(__name__)
_log.addHandler(stdout_stream)
_log.setLevel(logging.DEBUG)


class MyMaster:
    """
        Interface for all master application callback info except for measurement values.
        DNP3 spec section 5.1.6.1:
            The Application Layer provides the following services for the DNP3 User Layer in a master:
                - Formats requests directed to one or more outstations.
                - Notifies the DNP3 User Layer when new data or information arrives from an outstation.
        DNP spec section 5.1.6.3:
            The Application Layer requires specific services from the layers beneath it.
                - Partitioning of fragments into smaller portions for transport reliability.
                - Knowledge of which device(s) were the source of received messages.
                - Transmission of messages to specific devices or to all devices.
                - Message integrity (i.e., error-free reception and transmission of messages).
                - Knowledge of the time when messages arrive.
                - Either precise times of transmission or the ability to set time values
                  into outgoing messages.
    """
    _values = {'analog': [], 'binary': []}

    def _setValues(self, values):
        self._values = values

    def _getValues(self):
        return self._values

    values = property(_getValues, _setValues)
    def __init__(self,
                 log_handler=asiodnp3.ConsoleLogger().Create(),
                 listener=asiodnp3.PrintingChannelListener().Create(),
                 soe_handler=asiodnp3.PrintingSOEHandler().Create(),
                 master_application=asiodnp3.DefaultMasterApplication().Create(),
                 stack_config=None,
                 outstation_address="127.0.0.1",
                 outstation_id=1024, type="tcp"):

        _log.debug('Creating a DNP3Manager.')
        self.log_handler = log_handler
        self.manager = asiodnp3.DNP3Manager(1, self.log_handler)

        _log.debug('Creating the DNP3 channel, a TCP client.')
        self.retry = asiopal.ChannelRetry().Default()
        self.listener = listener
        if type == "tcp":
            self.channel = self.manager.AddTCPClient("tcpclient",
                                                 FILTERS,
                                                 self.retry,
                                                 outstation_address,
                                                 LOCAL,
                                                 PORT,
                                                 self.listener)
        if type == "serial":
            self.serial_settings = asiopal.SerialSettings()
            self.serial_settings.deviceName = outstation_address
            self.serial_settings.baud = 9600
            self.serial_settings.dataBits = 8
            self.channel = self.manager.AddSerial("server", FILTERS, self.retry, self.serial_settings,
                                                  self.listener)

        _log.debug('Configuring the DNP3 stack.')
        self.stack_config = stack_config
        if not self.stack_config:
            self.stack_config = asiodnp3.MasterStackConfig()
            self.stack_config.master.responseTimeout = openpal.TimeDuration().Seconds(10)
            self.stack_config.link.RemoteAddr = outstation_id

        _log.debug('Adding the master to the channel.')
        self.soe_handler = soe_handler
        self.soe_handler.values = self.values
        self.master_application = master_application
        self.master = self.channel.AddMaster("master",
                                   self.soe_handler,# asiodnp3.PrintingSOEHandler().Create(),
                                   self.master_application,
                                   self.stack_config)

        _log.debug('Configuring some scans (periodic reads).')
        # # Set up a "slow scan", an infrequent integrity poll that requests events and static data for all classes.
        # self.slow_scan = self.master.AddClassScan(opendnp3.ClassField().AllClasses(),
        #                                           openpal.TimeDuration().Minutes(30),
        #                                           opendnp3.TaskConfig().Default())
        # # Set up a "fast scan", a relatively-frequent exception poll that requests events and class 1 static data.
        # self.fast_scan = self.master.AddClassScan(opendnp3.ClassField(opendnp3.ClassField.CLASS_1),
        #                                           openpal.TimeDuration().Minutes(1),
        #                                           opendnp3.TaskConfig().Default())

        self.channel.SetLogFilters(openpal.LogFilters(opendnp3.levels.ALL_COMMS))
        self.master.SetLogFilters(openpal.LogFilters(opendnp3.levels.ALL_COMMS))

        _log.debug('Enabling the master. At this point, traffic will start to flow between the Master and Outstations.')
        self.master.Enable()
        time.sleep(5)

    def send_direct_operate_command(self, command, index, callback=asiodnp3.PrintingCommandCallback.Get(),
                                    config=opendnp3.TaskConfig().Default()):
        """
            Direct operate a single command
        :param command: command to operate
        :param index: index of the command
        :param callback: callback that will be invoked upon completion or failure
        :param config: optional configuration that controls normal callbacks and allows the user to be specified for SA
        """
        self.master.DirectOperate(command, index, callback, config)

    def send_direct_operate_command_set(self, command_set, callback=asiodnp3.PrintingCommandCallback.Get(),
                                        config=opendnp3.TaskConfig().Default()):
        """
            Direct operate a set of commands
        :param command_set: set of command headers
        :param callback: callback that will be invoked upon completion or failure
        :param config: optional configuration that controls normal callbacks and allows the user to be specified for SA
        """
        self.master.DirectOperate(command_set, callback, config)

    def send_select_and_operate_command(self, command, index, callback=asiodnp3.PrintingCommandCallback.Get(),
                                        config=opendnp3.TaskConfig().Default()):
        """
            Select and operate a single command
        :param command: command to operate
        :param index: index of the command
        :param callback: callback that will be invoked upon completion or failure
        :param config: optional configuration that controls normal callbacks and allows the user to be specified for SA
        """
        self.master.SelectAndOperate(command, index, callback, config)

    def send_select_and_operate_command_set(self, command_set, callback=asiodnp3.PrintingCommandCallback.Get(),
                                            config=opendnp3.TaskConfig().Default()):
        """
            Select and operate a set of commands
        :param command_set: set of command headers
        :param callback: callback that will be invoked upon completion or failure
        :param config: optional configuration that controls normal callbacks and allows the user to be specified for SA
        """
        self.master.SelectAndOperate(command_set, callback, config)

    def shutdown(self):
        # del self.slow_scan
        # del self.fast_scan
        del self.channel
        del self.master
        self.manager.Shutdown()

    def pause(self):
        self.master.Disable()

    def resume(self):
        self.master.Enable()
        time.sleep(15)


class MyLogger(openpal.ILogHandler):
    """
        Override ILogHandler in this manner to implement application-specific logging behavior.
    """

    def __init__(self):
        super(MyLogger, self).__init__()

    def Log(self, entry):
        flag = opendnp3.LogFlagToString(entry.filters.GetBitfield())
        filters = entry.filters.GetBitfield()
        location = entry.location.rsplit('/')[-1] if entry.location else ''
        message = entry.message
        _log.debug('LOG\t\t{:<10}\tfilters={:<5}\tlocation={:<25}\tentry={}'.format(flag, filters, location, message))


class AppChannelListener(asiodnp3.IChannelListener):
    """
        Override IChannelListener in this manner to implement application-specific channel behavior.
    """

    def __init__(self):
        super(AppChannelListener, self).__init__()

    def OnStateChange(self, state):
        _log.debug('In AppChannelListener.OnStateChange: state={}'.format(opendnp3.ChannelStateToString(state)))


class SOEHandler(opendnp3.ISOEHandler):
    """
        Override ISOEHandler in this manner to implement application-specific sequence-of-events behavior.
        This is an interface for SequenceOfEvents (SOE) callbacks from the Master stack to the application layer.
    """

    def __init__(self):
        self._values = {'analog': [], 'binary': []}
        super(SOEHandler, self).__init__()

    def Process(self, info, values):
        a_vals = []
        b_vals = []

        if (type(values) == opendnp3.ICollectionIndexedAnalog):
            class BOSVisitor(opendnp3.IVisitorIndexedAnalog):
                def __init__(self):
                    super(BOSVisitor, self).__init__()

                def OnValue(self, indexed_instance):
                    a_vals.append(indexed_instance.value.value)

            values.Foreach(BOSVisitor())
            self.values['analog'] = a_vals.copy()

        if (type(values) == opendnp3.ICollectionIndexedBinary):
            class BOSVisitorBin(opendnp3.IVisitorIndexedBinary):
                def __init__(self):
                    super(BOSVisitorBin, self).__init__()

                def OnValue(self, indexed_instance):
                    b_vals.append(indexed_instance.value.value)

            values.Foreach(BOSVisitorBin())
            print("here")
            self.values['binary'] = b_vals.copy()

    def Start(self):
        # This is implementing an interface, so this function
        # must be declared.
        pass

    def End(self):
        # This is implementing an interface, so this function
        # must be declared.
        pass


class MasterApplication(opendnp3.IMasterApplication):
    def __init__(self):
        super(MasterApplication, self).__init__()

    # Overridden method
    def AssignClassDuringStartup(self):
        _log.debug('In MasterApplication.AssignClassDuringStartup')
        return False

    # Overridden method
    def OnClose(self):
        _log.debug('In MasterApplication.OnClose')

    # Overridden method
    def OnOpen(self):
        _log.debug('In MasterApplication.OnOpen')

    # Overridden method
    def OnReceiveIIN(self, iin):
        _log.debug('In MasterApplication.OnReceiveIIN')

    # Overridden method
    def OnTaskComplete(self, info):
        _log.debug('In MasterApplication.OnTaskComplete')

    # Overridden method
    def OnTaskStart(self, type, id):
        _log.debug('In MasterApplication.OnTaskStart')


def collection_callback(result=None):
    """
    :type result: opendnp3.CommandPointResult
    """
    global RESULTS
    RESULTS.clear()
    print("Header: {0} | Index:  {1} | State:  {2} | Status: {3}".format(
        result.headerIndex,
        result.index,
        opendnp3.CommandPointStateToString(result.state),
        opendnp3.CommandStatusToString(result.status)
    ))
    set = {"header":result.headerIndex,
        "index": result.index,
        "state": opendnp3.CommandPointStateToString(result.state),
        "status": opendnp3.CommandStatusToString(result.status)}
    RESULTS.append(set)


def command_callback(result=None):
    """
    :type result: opendnp3.ICommandTaskResult
    """
    print("Received command result with summary: {}".format(opendnp3.TaskCompletionToString(result.summary)))
    result.ForeachItem(collection_callback)


def restart_callback(result=opendnp3.RestartOperationResult()):
    if result.summary == opendnp3.TaskCompletion.SUCCESS:
        print("Restart success | Restart Time: {}".format(result.restartTime.GetMilliseconds()))
    else:
        print("Restart fail | Failure: {}".format(opendnp3.TaskCompletionToString(result.summary)))