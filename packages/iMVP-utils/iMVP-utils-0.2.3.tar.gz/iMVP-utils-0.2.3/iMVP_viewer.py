#! /usr/bin/env python3
from ensurepip import version
import sys, os
import argparse
from iMVP_utils.interactive import launch_backend

if __name__ == "__main__":
    """The iMVP modification viewer application.
    Parameters
    ----------
    --output, -out: str
        The path used for storing the files (figures, fasta, etc.).
    --host: str
        The IP address of the sever.
    --port: int
        The port id.
    """
    parser = argparse.ArgumentParser(prog="iMVP_viewer")
    parser.add_argument('--output','-o', dest="output_path", type = str, default="./output/",help='The output directory. If not exist, will make the folder. Default="./output/"')
    parser.add_argument('--host', dest="host", type = str, default="127.0.0.1",help='The IP address of the app, default=127.0.0.1 (localhost)')
    parser.add_argument('--port', dest="port", type = int, default=8050,help='The port number that you want to dispaly the app.')
    parser.add_argument('--version', '-v', action='version', version="0.2.3",help='Display version.')

    options = parser.parse_args()

    host_ip_address = options.host
    port_id = options.port
    output_path = options.output_path
    app = launch_backend(output_path=output_path)

    app.run_server(debug=True, host=host_ip_address, port=port_id) 