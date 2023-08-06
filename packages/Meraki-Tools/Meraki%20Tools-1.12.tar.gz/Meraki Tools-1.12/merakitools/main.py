"""
    Main Module of autosync Application
"""
import asyncio
from merakitools import meraki_tasks
from merakitools import const, lib, model, utils
from merakitools.model import golden_nets, meraki_nets


def setup_app(cfg_file=None):
	const.appcfg = model.APPCONFIG(cfg_file)
	temp_sdk = lib.MerakiApi()
	const.meraki_sdk = temp_sdk.api


def run(cfg_file=None,task='sync',device_task=None):
	"""
    Main Module Start of Application
    Args:
    Returns:

    """
	setup_app(cfg_file)
	if task == 'sync':
		asyncio.run(meraki_tasks.sync_task())
	elif task == 'device_config':
		asyncio.run(meraki_tasks.device_config(device_task))
	
	

if __name__ == '__main__':
	config_file = '~/apps/testSync/ciscolab-config.json'
	run(config_file,"sync")
	print('Done')
