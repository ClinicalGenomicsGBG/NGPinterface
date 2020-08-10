import os
import hashlib

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def calculate_etag(local_path):
    file_size = os.stat(local_path).st_size
    size_threshold = int(config.get('hcp', 'size_threshold'))

    chunk_size = int(config.get('hcp', 'chunk_size'))
    if file_size > size_threshold:

        chunk_hashes = []
        with open(local_path, 'rb') as fp:
            while chunk := fp.read(chunk_size):
                chunk_hashes.append(hashlib.sha256(chunk))

        binary_digests = b''.join(chunk_hash.digest() for chunk_hash in chunk_hashes)
        binary_hash = hashlib.sha256(binary_digests).hexdigest()
        return f'"{binary_hash}-{len(chunk_hashes)}"'

    else:
        file_hash = hashlib.md5()
        with open(local_path, 'rb') as fp:
            while chunk := fp.read(chunk_size):
                file_hash.update(chunk)

        return f'"{file_hash.hexdigest()}"'