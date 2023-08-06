import os
import click
from merakitools.api.server import app

@click.group()
def cli():
	""" Start Meraki SYNC API Server """
	pass


@click.command(name='start',help="Starts API Server")

def start():
	app.run(host="0.0.0.0",port=5050)


cli.add_command(start)