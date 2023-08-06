"""
    Main Module of autosync Application
"""
import asyncio
from os import getenv
from merakitools import meraki_tasks
from merakitools import const, lib, model, utils
from merakitools.model import golden_nets, meraki_nets


def setup_app(cfg_file=None):
	const.appcfg = model.APPCONFIG(cfg_file)
	temp_sdk = lib.MerakiApi()
	const.meraki_sdk = temp_sdk.api


def run(cfg_file=None,task='sync',device_task=None,network_name=None):
	"""
    Main Module Start of Application
    Args:
    Returns:

    """
	setup_app(cfg_file)
	if task == 'sync':
		asyncio.run(meraki_tasks.sync_task(network_name=network_name))
		return "Sync Complete"
	elif task == 'device_config':
		asyncio.run(meraki_tasks.device_config(device_task))
	
	

if __name__ == '__main__':
	#config_file = '~/apps/testSync/ciscolab-config.json'
	config_file=None
	network_name = "29Q892"
	if config_file is None:
		config_file = getenv("MERAKI_TOOLS_CONFIG", None)
	#run(config_file,"sync",network_name="29Q892")
	run(config_file,"sync",network_name="29Q892,09X055,07X018,15B029,15B094,02M041")
	#run(config_file, "sync")
	print('Done')
