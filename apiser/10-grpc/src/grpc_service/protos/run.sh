#!/bin/sh
#pip install git+https://github.com/vmagamedov/grpclib.git
python -m grpc_tools.protoc -I. --python_out=../ --grpc_python_out=../ --python_grpc_out=../ ./*.proto
