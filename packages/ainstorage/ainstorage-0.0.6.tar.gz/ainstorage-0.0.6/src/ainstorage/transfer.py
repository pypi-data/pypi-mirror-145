import ast
import os
import firebase_admin
from firebase_admin import storage

from encrypt_manager import encrypt_file, decrypt_file
from auth import get_cred

class Transfer:
    def is_file(self, src_path):
        cred = get_cred()
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'kube-codelab-264608.appspot.com'
            })

        bucket = storage.bucket()
        blob = bucket.blob(src_path)
        
        return blob.exists()

    def upload_local(self, src_path, options):
        cred = get_cred()
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'kube-codelab-264608.appspot.com'
            })

        # open file
        src_file = open(src_path, 'rb')

        # create bucket and blob with file name
        bucket = storage.bucket()
        blob = None
        if options['dest_path']:
            blob = bucket.blob(options['dest_path'])
        else:
            blob = bucket.blob(os.path.basename(src_path))

        encryption_info = options['encryption_info']
        if options['do_encrypt']:
            cipher_dic = encrypt_file(src_file, encryption_info['secret_key'])
            # upload encrypted file
            blob.upload_from_string(str(cipher_dic))
        else:
            # upload from filename
            blob.upload_from_string(src_file.read())
    
    def download_local(self, src_path, dest_path, options):
        cred = get_cred()
        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'kube-codelab-264608.appspot.com'
            })

        # create bucket and blob with file name
        bucket = storage.bucket()
        blob = bucket.blob(src_path)

        # assign default value to dest_path
        if not dest_path:
            dest_path = os.path.basename(src_path)

        if options['is_encrypted']:
            decryption_info = options['decryption_info']

            blob.download_to_filename(dest_path + '.enc')
            # open file and get cipher_dic
            dest_file = open(dest_path + '.enc', 'r')
            cipher_dic = ast.literal_eval(dest_file.read())
            nonce = cipher_dic['nonce']
            tag = cipher_dic['tag']
            cipher_text = cipher_dic['cipher_text']

            secret_key = decryption_info['secret_key']
            decrypted_data = decrypt_file(nonce, tag, cipher_text, secret_key)

            # write file
            file_out = open(dest_path, 'wb')
            file_out.write(decrypted_data)
            file_out.close()
        else:
            blob.download_to_filename(dest_path)
    
    def download_ain(self, src_path, dest_path, options):
        print('TBD')
