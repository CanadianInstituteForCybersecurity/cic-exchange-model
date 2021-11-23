import os
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from modbus.ModbusTransceiver import ModbusTransceiver
from dnp3.DNP3Transceiver import execute_command
from multiprocessing import Process, Queue
from iec61850.mms import MMSTransceiver

app = Flask(__name__)
dxl_address = os.environ.get('DXL_ADDRESS')
dxl_port = os.environ.get('DXL_PORT')


@app.route('/query', methods=['POST'])
def query():  # version 2 parsing customSTIX object
    if not request.json or not 'type' in request.json:
        abort(400)

    if request.json['type'] == "modbus":
        host = request.json['host']
        unit_id = request.json['unit_id_hex']
        comm_type = request.json['comm_type']
        modbus_tx = ModbusTransceiver(comm_type=comm_type, host=host, unit_id=unit_id)
        command_params = {}
        for key in request.json["command_params"]:
            command_params[key] = request.json["command_params"][key]
        return jsonify({'modbus_query_' + comm_type: modbus_tx.query(command_params)}), 201
    elif request.json['type'] == "dnp3":
        host = request.json['host']
        comm_type = request.json['comm_type']
        outstation_id = request.json['outstation_id']
        command_params = {}
        for key in request.json["command_params"]:
            command_params[key] = request.json["command_params"][key]
        send_queue = Queue()
        recv_queue = Queue()
        recv_queue.put(command_params)
        process = Process(target=execute_command, args=(host, outstation_id, comm_type, recv_queue, send_queue))
        process.daemon = True
        process.start()
        result = send_queue.get()
        return jsonify({'dnp3_query_' + comm_type: result}), 201
    elif request.json["type"] == "mms":
        host = request.json['host']
        command_params = {}
        for key in request.json["command_params"]:
            command_params[key] = request.json["command_params"][key]

        mms_tx = MMSTransceiver.MMSTransceiver(host, 8102)
        result = mms_tx.query(command_params)
        return jsonify({'mms_query': result}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)


if __name__ == '__main__':
    app.run(host=dxl_address, port=dxl_port, debug=True)
