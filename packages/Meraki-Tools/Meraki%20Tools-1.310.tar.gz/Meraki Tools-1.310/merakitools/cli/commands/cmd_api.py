import os
import click
from merakitools.api.server import app

@click.group()
def cli():
	""" Start Meraki SYNC API Server """
	pass


@click.command(name='start',help="Starts API Server")
@click.option('--debug/--no-debug', help="Enables Debug Mode",default=False)
def start(debug):
	if debug:
		app.run(debug=True,host="0.0.0.0",port=5050)
	else:
		app.run(host="0.0.0.0",port=5050)


cli.add_command(start)