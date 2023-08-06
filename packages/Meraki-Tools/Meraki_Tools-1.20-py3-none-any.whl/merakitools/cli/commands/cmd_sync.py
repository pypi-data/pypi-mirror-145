import asyncio
import click
from merakitools.main import run
from merakitools import const

@click.group()
def cli():
    """ Tasks to start sync of Meraki Networks based on a golden/target tag """
    pass


@click.command(help='Starts Meraki Dashboard sync')
@click.option('-a', '--allOrgs')
@click.option('-c', '--useCache')
@click.option('-d','--debug')
@click.option('-f','--configfile',help="Full path and file name to .json configuration file EX: ~/merakitools/allOrgs-config.json")
@click.option('-k', '--merakiApiKey')
@click.option('-m', '--goldenTag')
@click.option('-o', '--autoSyncOrgs')
@click.option('-s', '--suppressLogging')
@click.option('-t', '--targetTag')
@click.option('-T', '--cacheTimeOut')
@click.option('-w', '--write')
@click.option('--tagOverRide')
def start(suppresslogging=None, merakiapikey=None, write=None, allorgs=None, autosyncorgs=None,
          usecache=None, cachetimeout=None, goldentag=None, targettag=None, tagoverride=None,
          logginglevel=None,configfile=None,debug=None):
    if configfile is not None:
        run(configfile, 'sync')

    else:
        cfg = {'suppress_logging'        : suppresslogging,
               'MERAKI_DASHBOARD_API_KEY': merakiapikey,
               'write'                   : write,
               'whitelist'               : autosyncorgs,
               'tag_golden'              : goldentag,
               'tag_target'              : targettag,
               'all_orgs'                : allorgs,
               'use_cache'               : usecache,
               'cache_timeout'           : cachetimeout,
               'tag_override'            : tagoverride,
               'logging_level'           : logginglevel,
               'debug'                   : debug}
        
        asyncio.run(run(cfg))
        





cli.add_command(start)
