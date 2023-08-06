import os.path
import json
from firebase_admin import credentials
from pathlib import Path

def get_cred():
    curr_dir = os.getcwd()
    os.chdir(os.path.expanduser('~') + '/.ainstorage')
    cred = credentials.Certificate('kube-codelab.json')

    os.chdir(curr_dir)
    return cred

def get_secret_key():
    curr_dir = os.getcwd()
    os.chdir(os.path.expanduser('~') + '/.ainstorage')
    
    secret_key_src = Path('secret_key.json')
    if not secret_key_src.is_file():
        from .encrypt_manager import generate_secret_key
        secret_key = generate_secret_key()
        
        secret_key_json = {
            'secret_key': secret_key
        }

        secret_key_file = open('secret_key.json', 'w')
        secret_key_file.write(json.dumps(secret_key_json))
        secret_key_file.close()

        os.chdir(curr_dir)
        return secret_key
    else:
        secret_key_file = open('secret_key.json', 'r')
        secret_key_json = json.loads(secret_key_file.read())

        os.chdir(curr_dir)
        return secret_key_json['secret_key']

def renew_secret_key():
    print('TBD')


def get_pre_bls_12381_key():
    curr_dir = os.getcwd()
    os.chdir(os.path.expanduser('~') + '/.ainstorage')
    
    pre_key_src = Path('pre_key.json')
    if not pre_key_src.is_file():
        from .lib.pre_bls12381 import PRE_BSL12381
        pk, sk = PRE_BSL12381().gen_pre_key()
        
        pre_key = {
            'pk': pk.hex(),
            'sk': sk.hex()
        }

        pre_key_file = open('pre_key.json', 'w')
        pre_key_file.write(json.dumps(pre_key))
        pre_key_file.close()

        os.chdir(curr_dir)
        return pk, sk
    else:
        pre_file = open('pre_key.json', 'r')
        pre_key = json.loads(pre_file.read())

        pk = bytearray.fromhex(pre_key['pk'])
        sk = bytearray.fromhex(pre_key['sk'])

        os.chdir(curr_dir)
        return pk, sk

def get_pre_ed25519_signing_key():
    curr_dir = os.getcwd()
    os.chdir(os.path.expanduser('~') + '/.ainstorage')
    
    signing_key_src = Path('signing_key.json')
    if not signing_key_src.is_file():
        from .lib.pre_bls12381 import PRE_BSL12381
        spk, ssk = PRE_BSL12381().gen_signing_key()
        
        signing_key = {
            'spk': spk.hex(),
            'ssk': ssk.hex()
        }

        signing_key_file = open('signing_key.json', 'w')
        signing_key_file.write(json.dumps(signing_key))
        signing_key_file.close()

        os.chdir(curr_dir)
        return spk, ssk
    else:
        signing_key_file = open('signing_key.json', 'r')
        signing_key = json.loads(signing_key_file.read())

        spk = bytearray.fromhex(signing_key['spk'])
        ssk = bytearray.fromhex(signing_key['ssk'])

        os.chdir(curr_dir)
        return spk, ssk
