import click
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from transfer import Transfer
from auth import get_secret_key

@click.command(name='upload')
@click.argument('src', nargs=1, required=True)
@click.argument('dest', required=False)
@click.option('-e', '--encryption', is_flag=True, show_default=True, default=False)
@click.option('--ainetwork', is_flag=True, show_default=True, default=False, help='Upload file with ainetwork')
def upload_file(src, dest, encryption, ainetwork):
    transfer = Transfer()
    
    # check file existence
    if not Path(src).is_file():
        raise SystemExit('Source file is not exist')
    
    options = { }
    options['dest_path'] = dest
    if encryption:
        secret_key = get_secret_key()
        encryption_info = { 'secret_key': secret_key }
        options['encryption_info'] = encryption_info
        options['do_encrypt'] = True
    else:
        options['do_encrypt'] = False
    
    if ainetwork:
        print('TBD')
    else:
        transfer.upload_local(src, options)

    click.echo('uploaded')

@click.command(name='download')
@click.argument('src', nargs=1, required=True)
@click.argument('dest', required=False)
@click.option('-e', '--encrypted', is_flag=True, show_default=True, default=False)
@click.option('--ainetwork', is_flag=True, show_default=True, default=False, help='Download file with ainetwork')
def download_file(src, dest, encrypted, ainetwork):
    transfer = Transfer()
    
    # check file existence
    if not transfer.is_file(src):
        raise SystemExit('Source file is not exist')

    options = { }
    if encrypted:
        secret_key = get_secret_key()
        decryption_info = { 'secret_key': secret_key }
        options['decryption_info'] = decryption_info
        options['is_encrypted'] = True
    else:
        options['is_encrypted'] = False

    if ainetwork:
        print('TBD')
    else:
        transfer.download_local(src, dest, options)

    click.echo('downloaded')
