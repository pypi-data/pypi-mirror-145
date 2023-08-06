import click
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from auth import get_secret_key

@click.group()
def auth_cli():
    pass

@auth_cli.command(name='create-secret-key')
def create_secret_key():
    # this function returns secret key
    get_secret_key()
    click.echo('Secret key is created')

@auth_cli.command(name='create-wallet')
def create_wallet():
    click.echo('Wallet is created')
