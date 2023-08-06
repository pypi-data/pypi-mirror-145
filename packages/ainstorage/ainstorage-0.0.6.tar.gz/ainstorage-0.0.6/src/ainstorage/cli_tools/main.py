import click
from ainstorage.cli_tools.auth_cli import commands as auth_cli
from ainstorage.cli_tools.transfer_cli import commands as transfer_cli

@click.group()
def cli():
    pass

@cli.group('auth')
def auth():
    pass

cli.add_command(transfer_cli.upload_file)
cli.add_command(transfer_cli.download_file)

auth.add_command(auth_cli.create_secret_key)
auth.add_command(auth_cli.create_wallet)
