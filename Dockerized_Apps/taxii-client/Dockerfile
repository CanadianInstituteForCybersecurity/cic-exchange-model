FROM python:3

WORKDIR /taxii-client
 
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

ENV TAXII_SERVER_ADDRESS localhost
ENV TAXII_SERVER_PORT 5000
ENV TAXII_API_ROOT trustgroup1
ENV TAXII_COLLECTION 91a7b528-80eb-42ed-a74d-c6fbd5a26116
ENV DXL_ADDRESS localhost
ENV DXL_PORT 8000
ENV DXL_METHOD query
ENV PYTHONUNBUFFERED 1
ENV USERNAME admin
ENV PASSWORD Password0

CMD ["python","./main.py"]
