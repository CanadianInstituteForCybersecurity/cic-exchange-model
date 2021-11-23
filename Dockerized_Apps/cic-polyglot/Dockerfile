FROM python:3

WORKDIR /cic-polyglot

RUN apt update && apt -y install cmake swig git

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

RUN cd .. && git clone https://github.com/mz-automation/libiec61850.git && cd libiec61850 && cmake -DBUILD_PYTHON_BINDINGS=ON . && make

RUN cd /libiec61850/pyiec61850 && cp iec61850.py _iec61850.so /cic-polyglot/iec61850

ENV DXL_ADDRESS localhost
ENV DXL_PORT 8000

CMD ["python","./STIXFieldMapper.py"]
