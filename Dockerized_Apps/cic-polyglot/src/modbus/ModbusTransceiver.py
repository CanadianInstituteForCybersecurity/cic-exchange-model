import serial
from pyModbusTCP.client import ModbusClient
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst

class ModbusTransceiver():
    """
    Modbus Tranceiver receives a dict containing parameters which is used
    to query a Modbus server for information
    """
    def __init__(self, comm_type, host, unit_id):
        """Sets up the connection"""
        self.comm_type = comm_type
        if self.comm_type == "tcp":
            self.tcp_client = ModbusClient(host=host, port=502, unit_id=unit_id, auto_open=True, auto_close=True)
        elif self.comm_type == "rtu":
            self.rtu_client = modbus_rtu.RtuMaster(
                serial.Serial(port=host, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
            )
            self.rtu_client.set_timeout(5.0)
            self.rtu_client.set_verbose(True)
            self.slave_id = unit_id

    def query(self, command_params):
        """Queries Modbus server based on Modbus communication type"""
        if self.comm_type == "tcp":
            response = self.tcp_query(command_params)
            return response
        if self.comm_type == "rtu":
            response = self.rtu_query(command_params)
            return response

    def tcp_query(self, command_params):
        """Is responsible for making queries to Modbus TCP servers"""
        function_code = command_params["function_code_hex"]
        if function_code == 1:
            coils = self.tcp_client.read_coils(command_params["address_hex"], command_params["quantity_hex"])
            return coils
        elif function_code == 2:
            discrete_inputs = self.tcp_client.read_discrete_inputs(command_params["address_hex"], command_params["quantity_hex"])
            return discrete_inputs
        elif function_code == 3:
            holding_registers = self.tcp_client.read_holding_registers(command_params["address_hex"], command_params["quantity_hex"])
            return holding_registers
        elif function_code == 4:
            input_registers = self.tcp_client.read_input_registers(command_params["address_hex"], command_params["quantity_hex"])
            return input_registers
        elif function_code == 5:
            coil_status = self.tcp_client.write_single_coil(command_params["address_hex"], command_params["value_hex"])
            return coil_status
        elif function_code == 15:
            coil_status = self.tcp_client.write_multiple_coils(command_params["address_hex"], command_params["value_hex"])
            return coil_status
        elif function_code == 6:
            register_status = self.tcp_client.write_single_register(command_params["address_hex"], command_params["value_hex"])
            return register_status
        elif function_code == 16:
            register_status = self.tcp_client.write_multiple_registers(command_params["address_hex"], command_params["value_hex"])
            return register_status
        else:
            return "Error: function code mismatch"

    def rtu_query(self, command_params):
        """Is responsible for making queries to Modbus RTU slaves"""
        function_code = command_params["function_code_hex"]
        if function_code == 1:
            coils = self.rtu_client.execute(self.slave_id, cst.READ_COILS, command_params["address_hex"], command_params["quantity_hex"])
            return coils
        elif function_code == 2:
            discrete_inputs = self.rtu_client.execute(self.slave_id, cst.READ_DISCRETE_INPUTS,
                                                      command_params["address_hex"], command_params["quantity_hex"])
            return discrete_inputs
        elif function_code == 3:
            holding_registers = self.rtu_client.execute(self.slave_id, cst.READ_HOLDING_REGISTERS,
                                                        command_params["address_hex"], command_params["quantity_hex"])
            return holding_registers
        elif function_code == 4:
            input_registers = self.rtu_client.execute(self.slave_id, cst.READ_INPUT_REGISTERS,
                                                      command_params["address_hex"], command_params["quantity_hex"])
            return input_registers
        elif function_code == 5:
            coil_status = self.rtu_client.execute(self.slave_id, cst.WRITE_SINGLE_COIL,
                                                  command_params["address_hex"], output_value=command_params["value_hex"])
            return coil_status
        elif function_code == 15:
            coil_status = self.rtu_client.execute(self.slave_id, cst.WRITE_MULTIPLE_COILS,
                                                  command_params["address_hex"], output_value=command_params["value_hex"])
            return coil_status
        elif function_code == 6:
            register_status = self.rtu_client.execute(self.slave_id, cst.WRITE_SINGLE_REGISTER,
                                                      command_params["address_hex"], output_value=command_params["value_hex"])
            return register_status
        elif function_code == 16:
            register_status = self.rtu_client.execute(self.slave_id, cst.WRITE_MULTIPLE_COILS,
                                                      command_params["address_hex"], output_value=command_params["value_hex"])
            return register_status
        else:
            return "Error: function code mismatch"
